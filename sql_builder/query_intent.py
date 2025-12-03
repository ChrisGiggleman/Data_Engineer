# query_intent.py
from dataclasses import dataclass, field
from typing import List, Optional, Literal, Any

# Supported comparison operators
Operator = Literal["=", ">", "<", ">=", "<=", "!=", "LIKE", "IN", "BETWEEN"]
LogicalOp = Literal["AND", "OR"]


@dataclass
class FilterIntent:
    """
    Represents a single condition, e.g. join_date > '2024-01-01'
    logical: how this condition combines with the previous one (AND/OR).
    - field:
        * normal column name, e.g. "join_date"
        * or special values like "__count__" (for COUNT(*))
        * or "expr:<raw SQL>" (for advanced expressions)
    """
    field: str
    operator: Operator
    value: Any                  # str, list[str], or tuple[str, str] for BETWEEN
    logical: LogicalOp = "AND"  # default AND; later we can parse OR


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

    # Core query shape
    distinct: bool = False
    filters: List[FilterIntent] = field(default_factory=list)   # WHERE
    group_by: List[str] = field(default_factory=list)           # GROUP BY
    having: List[FilterIntent] = field(default_factory=list)    # HAVING
    sort: List[SortIntent] = field(default_factory=list)        # ORDER BY
    limit: Optional[int] = None                                 # LIMIT
