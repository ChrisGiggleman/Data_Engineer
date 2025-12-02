# query_intent.py
from dataclasses import dataclass, field
from typing import List, Optional, Literal

Operator = Literal["=", ">", "<", ">=", "<=", "!=", "LIKE"]


@dataclass
class FilterIntent:
    field: str
    operator: Operator
    value: str


@dataclass
class SortIntent:
    field: str
    direction: Literal["asc", "desc"] = "asc"


@dataclass
class QueryIntent:
    """
    Logical representation of what the user is asking for.
    This is what the NL parser produces and the SQL builder consumes.
    """
    entity: str                        # logical name, e.g. "members"
    fields: List[str] = field(default_factory=list)
    distinct: bool = False
    filters: List[FilterIntent] = field(default_factory=list)
    sort: List[SortIntent] = field(default_factory=list)
    limit: Optional[int] = None
