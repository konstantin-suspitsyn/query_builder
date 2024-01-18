from enum_query_builder import FrontendTypeFields
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

            # Check if all joins exist
            for dimension_table in selected_objects.get_dimension_tables():
                if not self.joins.has_join(list(selected_objects.get_fact_tables())[0], dimension_table):
                    raise RuntimeError("No join")
        elif len(selected_objects.get_dimension_tables()) > 1:

            from_table = self.__get_dimension_table_that_connects_with_others(selected_objects.get_dimension_tables())

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

        where.update(selected_objects[FrontendTypeFields.WHERE.value])
        calculation.update(selected_objects[FrontendTypeFields.CALCULATIONS.value])

        query = self.__generate_sql_text_for_one_data_table(select, calculation, where, from_table, join_tables)

        return query

    def generate_select_for_multiple_data_tables(self, selected_objects: FieldsForQuery) -> str:
        """
        Generates CTE queries with multiple data tables
        :param selected_objects:
        :return:
        """
        dimension_tables: set = selected_objects.get_dimension_tables()
        fact_tables: set = selected_objects.get_fact_tables()

        # Fast check if all joins exist
        for fact_table in fact_tables:
            if len(selected_objects[TableTypes.DATA.value][fact_table]["select"]) > 0:
                raise RuntimeError("Select on fact join")

            for dimension_table in dimension_tables:

                if not self.joins.has_join(fact_table, dimension_table):
                    raise RuntimeError("No join")

        # For CTE we should define which fields will be used for join
        # If for every fact table, joined dimension table has the same field(s)
        #   Those fields should be used for later join of two fact fields
        # If not then fact fields will be used

        pass

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

    def __get_dimension_table_that_connects_with_others(self, dimension_tables: set):
        """
        Selects dimension table that has joins with all others dimension tables in set
        :param dimension_tables: set of dimension tables
        :return: string with name of tables or raises an error
        """
        if len(dimension_tables) == 1:
            return dimension_tables.pop()

        for from_table in dimension_tables:

            for join_table in dimension_tables:
                if from_table == join_table:
                    continue
                if not self.joins.has_join(from_table, join_table):
                    break

            return from_table

        raise RuntimeError("No join")
