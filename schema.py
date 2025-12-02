# schema.py
import re
import json
from pathlib import Path
from typing import Dict, List, Optional


class SchemaConfig:
    """
    Loads and manages the schema & business alias configuration from JSON.
    This is how we map natural-language phrases to entities & columns.
    """

    def __init__(self, config_path: str | Path):
        self._path = Path(config_path)
        with self._path.open("r", encoding="utf-8") as f:
            self._data: Dict = json.load(f)

    # ---------- Entity resolution ----------

    def resolve_entity(self, text: str) -> Optional[str]:
        """
        Return the entity key (e.g. 'members') that best matches the text,
        based on configured aliases. Uses a simple longest-alias scoring.
        """
        text_low = text.lower()
        best_entity = None
        best_score = 0

        for entity_name, entity in self._data.get("entities", {}).items():
            aliases = entity.get("aliases", [])
            for alias in aliases:
                alias_low = alias.lower()
                if alias_low in text_low:
                    score = len(alias_low)
                    if score > best_score:
                        best_score = score
                        best_entity = entity_name

        return best_entity

    def get_table_for_entity(self, entity: str) -> Optional[str]:
        entity_data = self._data.get("entities", {}).get(entity)
        if not entity_data:
            return None
        return entity_data.get("table")

    def entities(self) -> List[str]:
        """Return a list of all configured entity keys."""
        return list(self._data.get("entities", {}).keys())

    # ---------- Field & bundle resolution ----------

    def bundle_for_entity(self, entity: str) -> List[str]:
        entity_data = self._data.get("entities", {}).get(entity, {})
        return entity_data.get("details_bundle", [])

    def resolve_fields_from_text(self, entity: str, text: str) -> List[str]:
        """
        Try to detect which fields/columns are mentioned in the text.

        - If the text mentions 'details' (even misspelled), we use the entity's bundle.
          We do a fuzzy match: any word containing 'detai' (covers 'details',
          'deatils', 'detials', etc.) will trigger the bundle.
        - We also scan column aliases and include any that match.
        """
        entity_data = self._data.get("entities", {}).get(entity, {})
        columns: Dict[str, Dict] = entity_data.get("columns", {})

        text_low = text.lower()
        fields: List[str] = []

        # Fuzzy match for "details" to catch typos like "deatils", "detials", etc.
        if re.search(r"detai\w*", text_low):
            bundle = self.bundle_for_entity(entity)
            fields.extend(bundle)

        # Look for explicit column aliases in text
        for col_name, col_info in columns.items():
            aliases = col_info.get("aliases", [])
            for alias in aliases:
                if alias.lower() in text_low and col_name not in fields:
                    fields.append(col_name)

        # Deduplicate while preserving order
        seen = set()
        unique_fields: List[str] = []
        for f in fields:
            if f not in seen:
                seen.add(f)
                unique_fields.append(f)

        return unique_fields

    def field_exists(self, entity: str, field: str) -> bool:
        entity_data = self._data.get("entities", {}).get(entity, {})
        return field in entity_data.get("columns", {})

    def get_column_aliases(self, entity: str) -> Dict[str, List[str]]:
        entity_data = self._data.get("entities", {}).get(entity, {})
        columns: Dict[str, Dict] = entity_data.get("columns", {})
        return {name: info.get("aliases", []) for name, info in columns.items()}

    def resolve_field_from_phrase(self, entity: str, phrase: str) -> Optional[str]:
        """
        Given a short phrase like 'join dates' or 'signup date',
        try to resolve it to a single column for the given entity,
        using alias matching and a simple longest-match scoring.
        """
        phrase_low = phrase.lower()
        entity_data = self._data.get("entities", {}).get(entity, {})
        columns: Dict[str, Dict] = entity_data.get("columns", {})

        best_field = None
        best_score = 0

        for col_name, col_info in columns.items():
            aliases = col_info.get("aliases", [])
            for alias in aliases:
                alias_low = alias.lower()
                if alias_low in phrase_low:
                    score = len(alias_low)
                    if score > best_score:
                        best_score = score
                        best_field = col_name

        return best_field
# schema.py
import re
import json
from pathlib import Path
from typing import Dict, List, Optional


class SchemaConfig:
    """
    Loads and manages the schema & business alias configuration from JSON.
    This is how we map natural-language phrases to entities & columns.
    """

    def __init__(self, config_path: str | Path):
        self._path = Path(config_path)
        with self._path.open("r", encoding="utf-8") as f:
            self._data: Dict = json.load(f)

    # ---------- Entity resolution ----------

    def resolve_entity(self, text: str) -> Optional[str]:
        """
        Return the entity key (e.g. 'members') that best matches the text,
        based on configured aliases. Uses a simple longest-alias scoring.
        """
        text_low = text.lower()
        best_entity = None
        best_score = 0

        for entity_name, entity in self._data.get("entities", {}).items():
            aliases = entity.get("aliases", [])
            for alias in aliases:
                alias_low = alias.lower()
                if alias_low in text_low:
                    score = len(alias_low)
                    if score > best_score:
                        best_score = score
                        best_entity = entity_name

        return best_entity

    def get_table_for_entity(self, entity: str) -> Optional[str]:
        entity_data = self._data.get("entities", {}).get(entity)
        if not entity_data:
            return None
        return entity_data.get("table")

    def entities(self) -> List[str]:
        """Return a list of all configured entity keys."""
        return list(self._data.get("entities", {}).keys())

    # ---------- Field & bundle resolution ----------

    def bundle_for_entity(self, entity: str) -> List[str]:
        entity_data = self._data.get("entities", {}).get(entity, {})
        return entity_data.get("details_bundle", [])

    def resolve_fields_from_text(self, entity: str, text: str) -> List[str]:
        """
        Try to detect which fields/columns are mentioned in the text.

        - If the text mentions 'details' (even misspelled), we use the entity's bundle.
          We do a fuzzy match: any word containing 'detai' (covers 'details',
          'deatils', 'detials', etc.) will trigger the bundle.
        - We also scan column aliases and include any that match.
        """
        entity_data = self._data.get("entities", {}).get(entity, {})
        columns: Dict[str, Dict] = entity_data.get("columns", {})

        text_low = text.lower()
        fields: List[str] = []

        # Fuzzy match for "details" to catch typos like "deatils", "detials", etc.
        if re.search(r"detai\w*", text_low):
            bundle = self.bundle_for_entity(entity)
            fields.extend(bundle)

        # Look for explicit column aliases in text
        for col_name, col_info in columns.items():
            aliases = col_info.get("aliases", [])
            for alias in aliases:
                if alias.lower() in text_low and col_name not in fields:
                    fields.append(col_name)

        # Deduplicate while preserving order
        seen = set()
        unique_fields: List[str] = []
        for f in fields:
            if f not in seen:
                seen.add(f)
                unique_fields.append(f)

        return unique_fields

    def field_exists(self, entity: str, field: str) -> bool:
        entity_data = self._data.get("entities", {}).get(entity, {})
        return field in entity_data.get("columns", {})

    def get_column_aliases(self, entity: str) -> Dict[str, List[str]]:
        entity_data = self._data.get("entities", {}).get(entity, {})
        columns: Dict[str, Dict] = entity_data.get("columns", {})
        return {name: info.get("aliases", []) for name, info in columns.items()}

    def resolve_field_from_phrase(self, entity: str, phrase: str) -> Optional[str]:
        """
        Given a short phrase like 'join dates' or 'signup date',
        try to resolve it to a single column for the given entity,
        using alias matching and a simple longest-match scoring.
        """
        phrase_low = phrase.lower()
        entity_data = self._data.get("entities", {}).get(entity, {})
        columns: Dict[str, Dict] = entity_data.get("columns", {})

        best_field = None
        best_score = 0

        for col_name, col_info in columns.items():
            aliases = col_info.get("aliases", [])
            for alias in aliases:
                alias_low = alias.lower()
                if alias_low in phrase_low:
                    score = len(alias_low)
                    if score > best_score:
                        best_score = score
                        best_field = col_name

        return best_field
