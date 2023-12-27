from enum_query_builder import TomlTableTableTypeFieldPossibleValues
from exceptions_query_builder import UnknownTableTypeProperty
from gather_db_structure import TablesInfoLoader


def get_table_from_field(long_field: str) -> str:
    """
    Helper function to get table from long_field name
    :param long_field: long_field from frontend
    :return: string with name of table
    """
    return long_field[:len(long_field.split(".")[:-1])]


class PreQueryBuilder:
    """
    Gets all types of data
    Builds non-language specific query for language specific worker
    """

    def __init__(self, dict_fields: dict, dict_table: dict) -> None:
        """
        Initialize class
        :param dict_fields: all fields with properties
        :param dict_table: dict with table and properties
        """
        self.dict_fields = dict_fields
        self.dict_table = dict_table

    def get_all_fields_for_query_and_sort(self, all_fields: list) -> dict:
        """
        Gets all fields for query and sort them by types od tables, fields and filters
        :param all_fields: list with fields [database.schema.table.field,]
        :return: dictionary with {table: field} structure
        """

        all_fields_by_table = {}

        # Generate all possible table types
        for table_type in TomlTableTableTypeFieldPossibleValues:
            all_fields_by_table[table_type.value] = {}

        for field in all_fields:
            current_table = get_table_from_field(field)
            current_table_type = self.dict_table[current_table]["type"]

            # TODO generate all table types from dictionary from if to for in dictionary
            if current_table == "data":
                all_fields_by_table["data_tables"][current_table]: {}
            elif current_table == "dimension":
                all_fields_by_table["dimension_tables"][current_table]: {}
            else:
                raise UnknownTableTypeProperty(current_table, current_table_type)

            if current_table in all_fields_by_table:
                all_fields_by_table[current_table] = []

            # TODO: check field and separate to joinable and unjoinable

            all_fields_by_table[current_table].append(field)

        return all_fields_by_table

    # TODO: посчитать сколько фактовых таблиц. Если много, то делать отдельные СTE
    # TODO: Посмотреть что с датами. Если есть группировки по датам, то группировать
    # TODO: Обязательная проверка всех соединений
    # TODO: Внедрить алгоритм Дейкстры


if __name__ == "__main__":
    tables_info_loader = TablesInfoLoader()
    join_dict = tables_info_loader.get_joins_by_table_dictionary()
