import enum


class QueryPostgreSQL(enum.Enum):
    """
    Специальные слова в запросах postgresql
    """
    SELECT = "select"
    FROM = "from"
    LEFT_JOIN = "left join"
    INNER_JOIN = "inner join"
    RIGHT_JOIN = "right join"
    ON = "on"
    AND = "and"
    LIMIT = "limit"
    SUM = "sum"
    GROUP_BY = "group by"
