from collections import UserDict

from query_builder.utils.enums_and_field_dicts import TomlStructure, AllFieldsForImport, FrontendTypeFields, TableTypes
from query_builder.utils.exceptions import NoMandatoryKeyException, UnknownFieldType, FieldsFromFrontendWrongValue, \
    UnknownTableType


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


class FieldsFromFrontend(UserDict):
    """
    Type from frontend to other types of query builder
    dictionary with fields from frontend
            {
                "select": [list of fields to select, ...],
                "calculations": [list of calculations],
                "where": {field: string with condition,...}
            }
    """

    def __init__(self, dictionary=None):

        if dictionary is None:
            dictionary = {}

        if isinstance(dictionary, dict):

            # Check if every value under key is list
            for key in dictionary:
                if not isinstance(dictionary[key], list):
                    raise FieldsFromFrontendWrongValue(key)

            # Create complete structure if some fields are missing
            for key in FrontendTypeFields:
                if key.value not in dictionary:
                    dictionary[key.value] = []

        super().__init__(dictionary)

    def get_fields_by_type(self, type_of_fields: str) -> list:
        possible_field_type_values = [ft.value for ft in FrontendTypeFields]
        if type_of_fields not in possible_field_type_values:
            raise UnknownFieldType(type_of_fields)

        return self.data[type_of_fields]


class FieldsForQuery(UserDict):

    def __init__(self, dictionary=None):

        if dictionary is None:
            dictionary = {}

        if isinstance(dictionary, dict):
            for key in TableTypes:
                if key.value not in dictionary:
                    dictionary[key.value] = {}

        if FrontendTypeFields.WHERE.value not in dictionary:
            dictionary[FrontendTypeFields.WHERE.value] = set()

        if FrontendTypeFields.CALCULATIONS.value not in dictionary:
            dictionary[FrontendTypeFields.CALCULATIONS.value] = set()

        super().__init__(dictionary)

    def get_fact_tables(self) -> set:
        tables = set()
        for key in self.data[TableTypes.DATA.value]:
            tables.add(key)

        return tables

    def get_dimension_tables(self) -> set:
        tables = set()
        for key in self.data[TableTypes.DIMENSION.value]:
            tables.add(key)

        return tables

    def remove_all_fact_tables_except_named(self, table_name: str):
        fact_tables = self.get_fact_tables()
        fact_tables.remove(table_name)

        for table in fact_tables:
            del self.data[TableTypes.DATA.value][table]

    def get_all_tables(self) -> set:
        all_tables = set()
        all_tables.update(self.get_dimension_tables())
        all_tables.update(self.get_fact_tables())
        return all_tables

    @staticmethod
    def __create_table_structure() -> dict:
        """
        Creates table structure for new table
        :return: table structure for new table
        """
        table_structure = dict()
        table_structure["select"] = set()
        table_structure["calculations"] = set()
        table_structure["where"] = set()
        table_structure["not_for_select"] = set()
        table_structure["join_tables"] = set()
        table_structure["fact_must_join_on"] = set()
        table_structure["no_join_fact"] = set()

        return table_structure

    def add_table_if_not_exist(self, table_name: str, table_type: str) -> None:
        """
        Add table to dictionary
        :param table_name: table name
        :param table_type: should be one of @class TableTypes
        :return:
        """
        possible_table_type_values = [tt.value for tt in TableTypes]
        if table_type not in possible_table_type_values:
            UnknownTableType(table_name, table_type)

        if table_name not in self.data[table_type]:
            self.data[table_type][table_name] = self.__create_table_structure()

    def add_fields_to_table(self, table_name: str, table_type: str, select: set | None, calculations: set | None,
                            where: set | None, join_tables: set | None) -> None:
        """
        Creates table if it doesn't exist and add fields
        :param table_name: table name
        :param table_type: should be one of @class TableTypes
        :param select: set of select fields. Could be None
        :param calculations: set of calculation fields. Could be None
        :param where: set of where statements. Could be None
        :param join_tables: set of join tables. Could be None
        :return:
        """
        self.add_table_if_not_exist(table_name, table_type)
        if select is not None:
            self.data[table_type][table_name]["select"].update(select)
        if select is not None:
            self.data[table_type][table_name]["where"].update(where)
        if select is not None:
            self.data[table_type][table_name]["calculations"].update(calculations)
        if select is not None:
            self.data[table_type][table_name]["join_tables"].update(join_tables)

    def add_standalone_where(self, where: set) -> None:
        """
        Adds standalone where to set
        :param where:
        :return:
        """
        self.data[FrontendTypeFields.WHERE.value].update(where)

    def add_standalone_calculation(self, calculations: set) -> None:
        """
        Adds standalone calculations to set
        :param calculations:
        :return:
        """
        self.data[FrontendTypeFields.CALCULATIONS.value].update(calculations)

    def add_data_tables_if_not_exist(self, data_tables: set) -> None:
        """

        :param data_tables: Set of data tables
        :return:
        """
        for data_table in data_tables:
            self.add_table_if_not_exist(data_table, TableTypes.DATA.value)

    def add_dimension_tables_if_not_exist(self, dimension_tables: set) -> None:
        """

        :param dimension_tables: Set of dimension tables
        :return:
        """
        for dimension_table in dimension_tables:
            self.add_table_if_not_exist(dimension_table, TableTypes.DIMENSION.value)


class CteFields(UserDict):
    """
    Dictionary for CTE
    Which fields to use for join of main cte and fact_tables CTEs in QueryGenerator class
    """
    def add_table_if_not_exists(self, table_name: str) -> None:
        if table_name not in self.data:
            self.data[table_name] = set()

    def add_field(self, table_name: str, fields_to_join: str):
        self.add_table_if_not_exists(table_name)
        self.data[table_name].add(fields_to_join)

    def update_field(self, table_name: str, fields_to_join: set):
        self.add_table_if_not_exists(table_name)
        self.data[table_name].update(fields_to_join)
