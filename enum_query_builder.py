import enum


class TomlTablesMandatoryFields(enum.Enum):
    """
    All mandatory fields for toml files in tables folder
    """

    TABLE = "table"
    SCHEMA = "schema"
    DATABASE = "database"
    TABLE_TYPE = "table_type"
    FIELDS = "fields"


class TomlTableTableTypeFieldPossibleValues(enum.Enum):
    """
    All possible values for TomlTablesMandatoryFields.TABLE_TYPE field
    """
    DATA = "data"
    DIMENSION = "dimension"


class TomlTableFieldMandatoryProperties(enum.Enum):
    """
    All mush-have properties for fields
    """
    TYPE = "type"
    SHOW = "show"


class TomlTableCalculationFieldMandatoryProperties(enum.Enum):
    """
    All mush-have properties for fields
    """
    CALCULATION = "calculation"
    WHERE = "where"
    FACT_MUST_JOIN_ON = "fact_must_join_on"


class TomlMandatoryJoins(enum.Enum):
    """
    All mandatory properties for toml in joins folder
    """
    FIRST_TABLE = "first_table"
    SCHEMA = "schema"
    DATABASE = "database"
    SECOND_TABLE = "second_table"


class TomlMandatoryJoinsForSecondTable(enum.Enum):
    """
    Mandatory fields for joins
    """
    HOW = "how"
    ON = "on"
