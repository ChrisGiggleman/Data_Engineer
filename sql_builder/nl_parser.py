# nl_parser.py
import re

from query_intent import QueryIntent, FilterIntent, SortIntent
from schema import SchemaConfig


def _contains_any(text: str, phrases: list[str]) -> bool:
    text_low = text.lower()
    return any(p.lower() in text_low for p in phrases)


def parse_nl_to_intent(prompt: str, schema: SchemaConfig) -> QueryIntent:
    """
    Rule-based natural language → QueryIntent parser.

    Supports (so far):
    - entity detection via aliases (with fallback if only one entity exists)
    - DISTINCT / "no duplicates"
    - field detection from 'details' (fuzzy) + column aliases
    - special filter: 'darknet forum' → breach_source='darknet_forum'
    - basic 'where field is value' pattern
    - IN filters: "<phrase> in a, b, c"
    - date filters around join_date:
        'joined after YYYY-MM-DD'
        'joined before YYYY-MM-DD'
        'joined between YYYY-MM-DD and YYYY-MM-DD'
    - GROUP BY detection from:
        'group by <phrase>', 'grouped by <phrase>', 'per <phrase>'
    - HAVING COUNT(*) from:
        'having count > N', 'having count >= N', etc.
    - 'top N' → LIMIT N
    - 'sorted by X in ascending/descending order' or 'order by X desc' → ORDER BY
    """
    text_low = prompt.lower()

    # 1. Resolve entity
    entity = schema.resolve_entity(prompt)

    # Fallback: if no entity matched but only one entity is defined, assume that one
    if not entity:
        all_entities = schema.entities()
        if len(all_entities) == 1:
            entity = all_entities[0]

    if not entity:
        raise ValueError(
            "Could not determine which entity (e.g. members, orders) "
            "the request is about. Please mention the entity name more explicitly "
            "or configure more aliases."
        )

    # 2. DISTINCT / no duplicates
    distinct = _contains_any(
        text_low,
        ["no duplicates", "no duplicate", "distinct", "unique", "deduplicated"],
    )

    # 3. Fields
    fields = schema.resolve_fields_from_text(entity, prompt)
    # If nothing detected, default to the entity's details bundle
    if not fields:
        fields = schema.bundle_for_entity(entity)

    # 4. WHERE-like filters
    filters: list[FilterIntent] = []

    # Special 'darknet forum' rule
    if "darknet forum" in text_low and schema.field_exists(entity, "breach_source"):
        filters.append(
            FilterIntent(field="breach_source", operator="=", value="darknet_forum")
        )

    # Generic "where X is Y" or "where X = Y" pattern (very naive)
    where_pattern = r"where\s+([\w\.]+)\s+(is|=)\s+([^\s,]+)"
    m = re.search(where_pattern, text_low)
    if m:
        field, _, value = m.groups()
        filters.append(FilterIntent(field=field, operator="=", value=value))

    # --- Date filters around join_date (or equivalent) ---

    # Determine the appropriate date field if present
    date_field = None
    # Simple rule: if entity has 'join_date', we prefer that for "joined" style phrases
    if schema.field_exists(entity, "join_date"):
        date_field = "join_date"

    # joined after YYYY-MM-DD
    after_match = re.search(r"joined\s+after\s+(\d{4}-\d{2}-\d{2})", text_low)
    if after_match and date_field:
        date_val = after_match.group(1)
        filters.append(
            FilterIntent(field=date_field, operator=">", value=date_val)
        )

    # joined before YYYY-MM-DD
    before_match = re.search(r"joined\s+before\s+(\d{4}-\d{2}-\d{2})", text_low)
    if before_match and date_field:
        date_val = before_match.group(1)
        filters.append(
            FilterIntent(field=date_field, operator="<", value=date_val)
        )

    # joined between YYYY-MM-DD and YYYY-MM-DD
    between_match = re.search(
        r"joined\s+between\s+(\d{4}-\d{2}-\d{2})\s+and\s+(\d{4}-\d{2}-\d{2})",
        text_low,
    )
    if between_match and date_field:
        d1, d2 = between_match.groups()
        filters.append(
            FilterIntent(
                field=date_field,
                operator="BETWEEN",
                value=(d1, d2),
            )
        )

    # --- IN filters: "<phrase> in a, b, c" ---
    # Example: "status in active, pending, blocked"
    # We'll map <phrase> to a column using resolve_field_from_phrase.
    in_pattern = re.compile(
        r"([A-Za-z_ ]+?)\s+in\s+([A-Za-z0-9_,\s'\"-]+)",
        flags=re.IGNORECASE,
    )
    in_match = in_pattern.search(prompt)
    if in_match:
        field_phrase_raw, values_raw = in_match.groups()
        field_phrase = field_phrase_raw.strip(" .,")

        # Avoid matching things like "sorted by"
        if "sorted by" not in field_phrase.lower():
            field_col = schema.resolve_field_from_phrase(entity, field_phrase)
            if field_col:
                # split values on commas
                raw_items = values_raw.split(",")
                values = []
                for item in raw_items:
                    val = item.strip(" '\".")
                    if val:
                        values.append(val)
                if values:
                    filters.append(
                        FilterIntent(
                            field=field_col,
                            operator="IN",
                            value=values,
                        )
                    )

    # 5. LIMIT: 'top N'
    limit = None
    top_match = re.search(r"\btop\s+(\d+)", text_low)
    if top_match:
        limit = int(top_match.group(1))

    # 6. GROUP BY detection
    group_by: list[str] = []

    # Pattern 1: "group by <phrase>" or "grouped by <phrase>"
    group_pattern = re.compile(
        r"\bgroup(?:ed)? by\s+([A-Za-z_ ]+?)(?:[,\.\n]|$)",
        flags=re.IGNORECASE,
    )
    for gm in group_pattern.finditer(prompt):
        phrase = gm.group(1).strip(" .,")

        field_col = schema.resolve_field_from_phrase(entity, phrase)
        if field_col and field_col not in group_by:
            group_by.append(field_col)

    # Pattern 2: "per <phrase>"  (e.g., "count of members per breach source")
    per_pattern = re.compile(
        r"\bper\s+([A-Za-z_ ]+?)(?:[,\.\n]|$)",
        flags=re.IGNORECASE,
    )
    for pm in per_pattern.finditer(prompt):
        phrase = pm.group(1).strip(" .,")

        field_col = schema.resolve_field_from_phrase(entity, phrase)
        if field_col and field_col not in group_by:
            group_by.append(field_col)

    # 7. HAVING (COUNT) detection: "having count > N", etc.
    having: list[FilterIntent] = []

    having_pattern = re.compile(
        r"\bhaving\s+count\s*(=|!=|>=|<=|>|<)\s*(\d+)",
        flags=re.IGNORECASE,
    )
    hm = having_pattern.search(text_low)
    if hm:
        op, num_str = hm.groups()
        # Use special field "__count__" which sql_builder renders as COUNT(*)
        having.append(
            FilterIntent(
                field="__count__",
                operator=op,  # type: ignore
                value=num_str,
            )
        )

    # 8. Sorting
    sort: list[SortIntent] = []

    field_phrase = None
    direction = "asc"

    # Pattern 1: "sorted by <something> in ascending/descending order"
    m1 = re.search(
        r"\bsorted by\s+(.+?)\s+in\s+(ascending|descending)\s+order",
        prompt,
        flags=re.IGNORECASE,
    )
    if m1:
        field_phrase = m1.group(1).strip(" .,")
        asc_desc_word = m1.group(2).lower()
        if asc_desc_word.startswith("desc"):
            direction = "desc"
    else:
        # Pattern 2: "order by <something> asc/desc"
        m2 = re.search(
            r"\border by\s+(.+?)\s+(asc|desc)\b",
            prompt,
            flags=re.IGNORECASE,
        )
        if m2:
            field_phrase = m2.group(1).strip(" .,")
            asc_desc_short = m2.group(2).lower()
            if asc_desc_short == "desc":
                direction = "desc"

    if field_phrase:
        # Map phrase like "join dates" or "usernames" → actual column name
        field_col = schema.resolve_field_from_phrase(entity, field_phrase)
        if field_col:
            sort.append(SortIntent(field=field_col, direction=direction))

    # 9. Build QueryIntent
    intent = QueryIntent(
        entity=entity,
        fields=fields,
        distinct=distinct,
        filters=filters,
        group_by=group_by,
        having=having,
        sort=sort,
        limit=limit,
    )
    return intent
