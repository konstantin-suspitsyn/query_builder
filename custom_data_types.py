from collections import UserDict

from enum_query_builder import TomlTableTableTypeFieldPossibleValues, FrontendTypeFields
from exceptions_query_builder import UnknownTableType


class FieldsForQuery(UserDict):

    def __init__(self, dictionary=None):

        if dictionary is None:
            dictionary = {}

        if isinstance(dictionary, dict):
            for key in TomlTableTableTypeFieldPossibleValues:
                if key.value not in dictionary:
                    dictionary[key.value] = {}

        print(dictionary)

        super().__init__(dictionary)

    def get_fact_tables(self) -> set:
        tables = set()
        for key in self.data[TomlTableTableTypeFieldPossibleValues.DATA.value]:
            tables.add(key)

        return tables

    def get_dimension_tables(self) -> set:
        tables = set()
        for key in self.data[TomlTableTableTypeFieldPossibleValues.DIMENSION.value]:
            tables.add(key)

        return tables

    def remove_all_fact_tables_except_named(self, table_name: str):
        fact_tables = self.get_fact_tables()
        fact_tables.remove(table_name)

        for table in fact_tables:
            del self.data[TomlTableTableTypeFieldPossibleValues.DATA.value][table]

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

    def add_table(self, table_name: str, table_type: str) -> None:
        """
        Add table to dictionary
        :param table_name: table name
        :param table_type: should be one of @class TomlTableTableTypeFieldPossibleValues
        :return:
        """
        possible_table_type_values = [tt.value for tt in TomlTableTableTypeFieldPossibleValues]
        if table_type not in possible_table_type_values:
            UnknownTableType(table_name, table_type)

        self.data[TomlTableTableTypeFieldPossibleValues.DATA.value][table_name] = self.__create_table_structure()


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
            for key in FrontendTypeFields:
                if key.value not in dictionary:
                    dictionary[key.value] = []

        super().__init__(dictionary)

    def get_fields_by_type(self, type_of_fields: str) -> list:
        possible_field_type_values = [ft.value for ft in FrontendTypeFields]
        if type_of_fields not in possible_field_type_values:
            # TODO: raise an error
            pass

        return self.data[type_of_fields]
