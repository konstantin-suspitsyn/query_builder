from typing import Set

from custom_data_types import FieldsForQuery
from enum_query_builder import TomlTableTableTypeFieldPossibleValues
from shortest_joins import ShortestDistance


class SelectCreator:

    CTE = "cte_"

    def __init__(self, tables_dict: dict):
        self.tables_dict = tables_dict
        self.joins: ShortestDistance = ShortestDistance()

    @staticmethod
    def count_data_tables(selected_objects: FieldsForQuery) -> int:
        """
        Count how many fact tables in query
        If we have more than one query, we have to work with CTE
        :return:
        """
        return len(selected_objects.get_fact_tables())

    def create_query(self, selected_objects: FieldsForQuery) -> str:
        pass

    def select_for_one_table(self, selected_objects: FieldsForQuery) -> str:
        pass


class SelectPostgres(SelectCreator):
    def create_query(self, selected_objects: FieldsForQuery) -> str:
        for fact_table in selected_objects.get_fact_tables():
            pass
        return ""

    def select_for_one_table(self, selected_objects: FieldsForQuery) -> str:
        select: set = set()
        calculation: set = set()
        where: set = set()
        join_tables: set = set()
        from_table: str = ""
        query = "SELECT\n"

        print(selected_objects.get_fact_tables())

        if len(selected_objects.get_fact_tables()) == 1:
            from_table = list(selected_objects.get_fact_tables())[0]
        elif len(selected_objects.get_dimension_tables()) > 1:
            from_table = list(selected_objects.get_dimension_tables())[0]
        else:
            # TODO: raise exception
            pass

        join_tables.update(selected_objects.get_fact_tables())
        join_tables.update(selected_objects.get_dimension_tables())
        join_tables.remove(from_table)

        for key in TomlTableTableTypeFieldPossibleValues:
            set_of_tables = list(selected_objects[key.value].keys())
            for table in set_of_tables:
                select.update(selected_objects[key.value][table]["select"])
                calculation.update(selected_objects[key.value][table]["calculations"])
                where.update(selected_objects[key.value][table]["where"])

        where.add(selected_objects["where"])

        query += "\n,".join(select)
        if len(calculation) > 0:
            query += "\n," + "\n,".join(calculation)

        query += "\nfrom {}".format(from_table)

        for end_table in join_tables:
            if not self.joins.get_join(from_table, end_table):
                # TODO: raise exception
                pass
            print(self.joins.get_join(from_table, end_table))

            for key in self.joins.get_join(from_table, end_table).keys():

                join_temp = self.joins.get_join(from_table, end_table)[key]

                query += "\n{} join {} \n on {}".format(join_temp["how"], end_table, join_temp["on"])

        if len(where) > 0:
            query += "\n where \n"
            query += "\nand ".join(where)

        if len(calculation) > 0:
            query += "\ngroup by\n"
            query += "\n,".join(select)

        return query
