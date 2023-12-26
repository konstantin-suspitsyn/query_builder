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
