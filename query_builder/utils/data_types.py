from collections import UserDict

from query_builder.utils.enums_and_field_dicts import TomlStructure, AllFieldsForImport
from query_builder.utils.exceptions import NoMandatoryKeyException


class TableImport(UserDict):
    """
    Base class for TOML import
    """

    def __init__(self, dictionary: dict, current_file_path: str, toml_fields: TomlStructure):
        """
        :param dictionary: what came from toml file
        :param current_file_path: path to toml file
        """

        if not isinstance(dictionary, dict):
            raise RuntimeError("Should be dictionary")

        for key in toml_fields.get_all_mandatory_fields():
            if key not in dictionary.keys():
                raise NoMandatoryKeyException(current_file_path, key)

        super().__init__(dictionary)


class TableTomlImport(TableImport):
    """
    Toml that is imported from tables folder for StructureGenerator class
    """

    def __init__(self, dictionary: dict, current_file_path: str):
        """
        :param dictionary: what came from toml file
        :param current_file_path: path to toml file
        """

        fields = AllFieldsForImport()
        toml_fields = TomlStructure(fields.get_table_fields())

        super().__init__(dictionary, current_file_path, toml_fields)


class JoinsTomlImport(TableImport):
    """
    Toml that is imported from tables folder for StructureGenerator class
    """

    def __init__(self, dictionary: dict, current_file_path: str):
        """
        :param dictionary: what came from toml file
        :param current_file_path: path to toml file
        """

        fields = AllFieldsForImport()
        toml_fields = TomlStructure(fields.get_join_fields())

        super().__init__(dictionary, current_file_path, toml_fields)


class FiltersTomlImport(TableImport):
    """
    Toml that is imported from tables folder for StructureGenerator class
    """

    def __init__(self, dictionary: dict, current_file_path: str):
        """
        :param dictionary: what came from toml file
        :param current_file_path: path to toml file
        """

        toml_fields = dictionary

        fields = AllFieldsForImport()
        super().__init__(toml_fields, current_file_path, fields.get_where_dictionary())
