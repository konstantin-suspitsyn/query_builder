from gather_db_structure import TablesInfoLoader


class PreQueryBuilder:
    """
    Gets all types of data
    Builds non-language specific query for language specific worker
    """

    def __init__(self, dict_fields: dict, joins_by_table: dict) -> None:
        """
        :param dict_fields: структура dict_fields:
        {select: [поля], where: [поля]}
        """
        self.dict_fields = dict_fields
        self.joins_by_table = joins_by_table

    def get_all_fields_for_query_and_sort(self, all_fields: list) -> dict:
        """
        Gets all fields for query and sort them by types od tables, fields and filters
        :param all_fields: list with fields [database.schema.table.field,]
        :return: dictionary with {table: field} structure
        """
        all_fields_by_table = {}
        for field in all_fields:
            current_table = self.__get_table_from_field(field)

            if current_table in all_fields_by_table:
                all_fields_by_table[current_table] = []

            # TODO: check field and separate to joinable and unjoinable

            all_fields_by_table[current_table].append(field)

        return all_fields_by_table

    @staticmethod
    def __get_table_from_field(long_field: str) -> str:
        """
        Helper function to get table from long_field name
        :param long_field: long_field from frontend
        :return: string with name of table
        """
        return long_field[:len(long_field.split(".")[:-1])]

    # TODO: посчитать сколько фактовых таблиц. Если много, то делать отдельные СTE
    # TODO: Посмотреть что с датами. Если есть группировки по датам, то группировать
    # TODO: Обязательная проверка всех соединений
    # TODO: Внедрить алгоритм Дейкстры


if __name__ == "__main__":
    tables_info_loader = TablesInfoLoader()
    join_dict = tables_info_loader.get_joins_by_table_dictionary()
