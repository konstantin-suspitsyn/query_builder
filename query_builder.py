from gather_db_structure import TablesInfoLoader


class TestWorker:

    def __init__(self, dict_fields: dict, joins_by_table: dict) -> None:
        """
        :param dict_fields: структура dict_fields:
        {select: [поля], where: [поля]}
        """
        self.dict_fields = dict_fields
        self.joins_by_table = joins_by_table

    def __get_all_tables_from_fields(self) -> set:
        list_of_tables = []
        list_of_fields = self.dict_fields["select"]
        for field in list_of_fields:
            list_of_tables.append(field[:field.rfind(".")])

        return set(list_of_tables)

    def count_joins_with_types(self):
        count_all_tables_by_joins = {}
        for key in self.joins_by_table:
            count_all_tables_by_joins[key] = {}

        for table in self.__get_all_tables_from_fields():
            for join_type in self.joins_by_table:
                if table not in self.joins_by_table[join_type]:
                    continue

                # посчитать кол-во прав


if __name__ == "__main__":
    tables_info_loader = TablesInfoLoader()
    join_dict = tables_info_loader.get_joins_by_table_dictionary()
