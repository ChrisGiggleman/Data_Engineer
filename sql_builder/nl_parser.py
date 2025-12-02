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
    - distinct / "no duplicates"
    - field detection from 'details' keyword + column aliases
    - filter for 'darknet forum' → breach_source='darknet_forum'
    - basic 'where field is value' pattern
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

    # 2. Distinct / no duplicates
    distinct = _contains_any(
        text_low,
        ["no duplicates", "no duplicate", "distinct", "unique", "deduplicated"]
    )

    # 3. Fields
    fields = schema.resolve_fields_from_text(entity, prompt)
    # If nothing detected, default to the entity's details bundle
    if not fields:
        fields = schema.bundle_for_entity(entity)

    # 4. Filters (very basic for v1)
    filters: list[FilterIntent] = []

    # Example rule: if "darknet forum" appears and entity has 'breach_source', add filter
    if "darknet forum" in text_low and schema.field_exists(entity, "breach_source"):
        filters.append(FilterIntent(field="breach_source", operator="=", value="darknet_forum"))

    # Generic "where X is Y" or "where X = Y" pattern (very naive)
    where_pattern = r"where\s+([\w\.]+)\s+(is|=)\s+([^\s,]+)"
    m = re.search(where_pattern, text_low)
    if m:
        field, _, value = m.groups()
        filters.append(FilterIntent(field=field, operator="=", value=value))

    # 5. Limit: 'top N'
    limit = None
    top_match = re.search(r"\btop\s+(\d+)", text_low)
    if top_match:
        limit = int(top_match.group(1))

    # 6. Sorting
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
        # Map phrase like "join dates" → actual column name
        field_col = schema.resolve_field_from_phrase(entity, field_phrase)
        if field_col:
            sort.append(SortIntent(field=field_col, direction=direction))

    # 7. Build QueryIntent
    intent = QueryIntent(
        entity=entity,
        fields=fields,
        distinct=distinct,
        filters=filters,
        sort=sort,
        limit=limit,
    )
    return intent
