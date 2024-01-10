from typing import Set

from custom_data_types import FieldsForQuery
from enum_query_builder import TomlTableTableTypeFieldPossibleValues
from shortest_joins import ShortestDistance
from utilities_query_builder import join_on_to_string


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
        query: str = ""
        data_tables = selected_objects.get_fact_tables()
        if len(data_tables) <= 1:
            query = self.select_for_one_table(selected_objects)
        if len(data_tables) > 1:
            query = self.select_for_multiple_fact_tables(selected_objects)

        return ""

    def select_for_one_table(self, selected_objects: FieldsForQuery) -> str:

        # TODO: рефактор с select_for_multiple_fact_tables

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

                query += "\n{} join {} \n on {}".format(join_temp["how"], end_table,
                                                        join_on_to_string(join_temp["on"]))

        if len(where) > 0:
            query += "\n where \n"
            query += "\nand ".join(where)

        if len(calculation) > 0:
            query += "\ngroup by\n"
            query += "\n,".join(select)

        return query

    def select_for_multiple_fact_tables(self, selected_objects) -> str:

        must_join_select = set()
        no_join_fact = set()

        cte = {}

        # For all tables
        for fact_table in selected_objects.get_fact_tables():
            must_join_select.update(selected_objects[TomlTableTableTypeFieldPossibleValues.DATA.value][fact_table][
                                        "fact_must_join_on"])
            no_join_fact.update(selected_objects[TomlTableTableTypeFieldPossibleValues.DATA.value][fact_table][
                                        "no_join_fact"])

        # for each_cte
        cte_no: int = 0
        for from_table in selected_objects.get_fact_tables():
            cte[cte_no] = {}

            select: set = set()
            calculation: set = set()
            where: set = set()
            join_tables: set = set()

            join_tables.update(selected_objects.get_dimension_tables())
            join_tables.update(selected_objects[TomlTableTableTypeFieldPossibleValues.DATA.value][from_table][
                                   "join_tables"])

            for table in selected_objects.get_dimension_tables():
                select.update(selected_objects[TomlTableTableTypeFieldPossibleValues.DIMENSION.value][table]["select"])
                calculation.update(selected_objects[TomlTableTableTypeFieldPossibleValues.DIMENSION.value][table][
                                       "calculations"])
                where.update(selected_objects[TomlTableTableTypeFieldPossibleValues.DIMENSION.value][table]["where"])

            where.add(selected_objects["where"])

            query = "SELECT\n"

            query += "\n,".join(select)

            if len(must_join_select) > 0:
                query += "\n," + "\n,".join(must_join_select)

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

            cte[cte_no]["query"] = query
            cte[cte_no]["select"] = set()
            cte[cte_no]["must_join_select"] = set()
            cte[cte_no]["select"].update(select)
            cte[cte_no]["must_join_select"].update(must_join_select)

            cte_no += 1

        print(cte)

        final_query = "with \n"
        cte = "({}) as cte_{}\n"

        return ""
