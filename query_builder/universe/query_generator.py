from query_builder.utils.data_types import FieldsForQuery
from query_builder.utils.enums_and_field_dicts import TableTypes
from query_builder.utils.utils import join_on_to_string
from shortest_joins import ShortestDistance


class QueryGenerator:
    """
    Generates query
    """

    joins: ShortestDistance
    tables_dict: dict

    def __init__(self, tables_dict: dict):
        # All tables
        self.tables_dict = tables_dict
        # ShortestDistance is singleton
        self.joins: ShortestDistance = ShortestDistance()

    def generate_select_for_one_data_table(self, selected_objects: FieldsForQuery) -> str:
        """
        Generates query for one fact table and any number of dimension tables
        :param selected_objects: selected objects. Must have only one data table
        :return: SQL query
        """

        # This block of variables is used for sql generator
        select: set = set()
        calculation: set = set()
        where: set = set()
        join_tables: set = set()
        from_table: str = ""

        query: str

        # Check if method used correctly
        if len(selected_objects.get_fact_tables()) > 1:
            raise RuntimeError("This method for structure with one fact table")

        if len(selected_objects.get_fact_tables()) == 1:
            from_table = list(selected_objects.get_fact_tables())[0]
        elif len(selected_objects.get_dimension_tables()) > 1:
            from_table = list(selected_objects.get_dimension_tables())[0]

        # Get all tables needed for query
        join_tables.update(selected_objects.get_fact_tables())
        join_tables.update(selected_objects.get_dimension_tables())

        # Remove table used in from
        if from_table not in join_tables:
            raise RuntimeError

        join_tables.remove(from_table)

        for key in TableTypes:
            list_of_tables = list(selected_objects[key.value].keys())
            for table in list_of_tables:
                select.update(selected_objects[key.value][table]["select"])
                calculation.update(selected_objects[key.value][table]["calculations"])
                where.update(selected_objects[key.value][table]["where"])

        query = self.__generate_sql_text_for_one_data_table(select, calculation, where, from_table, join_tables)

        return query

    def __generate_sql_text_for_one_data_table(self, select: set, calculation: set, where: set,
                                               from_table: str, join_tables: set) -> str:
        """
        Generates sql from one data table
        :param select:
        :param calculation:
        :param where:
        :param from_table:
        :param join_tables:
        :return:
        """

        query: str = "SELECT\n\t "
        group_by: str = "\nGROUP BY\n\t "
        calculation_select: str = ""
        select_query: str = ""
        from_query = "\nFROM {}\n".format(from_table)
        where_query = "\nWHERE\n\t"

        if len(select) > 0:
            select_query = "\n\t,".join(select)
            query += select_query
            calculation_select = "\t,"

        if len(calculation) > 0:
            calculation_select += "\t,".join(calculation)
            query += calculation_select

        query += from_query

        for end_table in join_tables:
            for key in self.joins.get_join(from_table, end_table).keys():
                join_temp = self.joins.get_join(from_table, end_table)[key]

                query += "\n{} join {} \n on {}".format(join_temp["how"], end_table,
                                                        join_on_to_string(join_temp["on"]))

        if len(where) == 1:
            where_query += list(where)[0]
        if len(where) > 1:
            where_query += " and ".join(["({})".format(f) for f in where])
        if len(where) > 0:
            query += where_query

        if (len(calculation) > 0) and (len(select) > 0):
            query += group_by
            query += select_query

        return query
