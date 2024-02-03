import copy

from query_builder.universe.possible_joins import AllPossibleJoins
from query_builder.utils.data_types import FieldsForQuery, CteFields
from query_builder.utils.enums_and_field_dicts import TableTypes, FieldType, FrontendTypeFields
from query_builder.utils.utils import join_on_to_string


class QueryGenerator:
    """
    Generates query
    Suitable for PostgreSQL
    """

    joins: AllPossibleJoins
    tables_dict: dict
    CTE_JOIN = "cte_join"

    CTE = "cte_{}"
    MAIN_JOIN_TABLE = "query_builder.public.dim_calendar"
    CALC_FIELD = "{}_calc_{}"
    COMBI = "combi"

    DIMENSION_SELECTS_K = "dimension_selects"
    MAIN_CTE = "main_cte"
    OUT_K = "out"
    QUERY_K = "query"
    SELECT_K = "select"
    CALCULATIONS_K = "calculations"
    ALL_CTE = "all_cte"
    WHERE_K = "where"

    def __init__(self, tables_dict: dict):

        # All tables
        self.tables_dict = tables_dict
        # ShortestDistance is singleton
        self.joins: AllPossibleJoins = AllPossibleJoins()

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
                table_ = list(selected_objects.get_fact_tables())[0]
                if not self.joins.has_join(table_, dimension_table):
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
                select.update(selected_objects[key.value][table][self.SELECT_K])
                # TODO: SYNC this with BBBB
                i: int = 0
                for c in selected_objects[key.value][table][self.CALCULATIONS_K]:
                    calculation.add("{} as {}".format(c, self.CALC_FIELD.format(from_table.split(".")[-1],
                                                                                i)))
                    i += 1
                where.update(selected_objects[key.value][table][self.WHERE_K])

        where.update(selected_objects[FrontendTypeFields.WHERE.value])

        query = self.__generate_sql_text_for_one_data_table(select, calculation, where, from_table, join_tables)

        return query

    def generate_select_for_multiple_data_tables(self, selected_objects: FieldsForQuery) -> str:
        """
        Generates CTE queries with multiple data tables
        It will have structure:

        with
             cte_0 as (
                         all fields for fact_table[0]
                        ,all dimension table fields
                     )
            ,cte_1 as (
                         all fields for fact_table[1]
                        ,all dimension table fields
                      )
            ,cte_i as (
                         all fields for fact_table[i]
                        ,all dimension table fields
                      )
            cte_main as (UNION of all non calculation fields)

        select
            fields
        from cte_main
            left join cte_0
            left join cte_1
            left join cte_i
        where if needed
        group by if needed

        :param selected_objects:
        :return: sql query string
        """
        dimension_tables: set = selected_objects.get_dimension_tables()
        fact_tables: set = selected_objects.get_fact_tables()

        # Fast check if all joins exist
        for fact_table in fact_tables:
            if len(selected_objects[TableTypes.DATA.value][fact_table][self.SELECT_K]) > 0:
                raise RuntimeError("Select on fact join")

            for dimension_table in dimension_tables:

                if not self.joins.has_join(fact_table, dimension_table):
                    raise RuntimeError("No join")

        # TODO: check if fact tables doesn't have any non-calculation fields

        # For CTE we should define which fields will be used for join
        # If for every fact table, joined dimension table has the same field(s)
        #   Those fields should be used for later join of two fact fields
        # If not then fact fields will be used

        # Main CTE fields
        # Main CTE is cte created from other CTEs
        dimension_select = CteFields()

        # Check if fact tables joins to the same field in dimension tables

        for dimension_table in dimension_tables:
            dimension_join_fields: dict = {}
            for fact_table in fact_tables:
                temp_join = self.joins.get_join(fact_table, dimension_table)
                last_join_table_no: int = max(list(temp_join.keys()))
                dimension_join_fields[fact_table] = {TableTypes.DIMENSION.value:
                                                     set(temp_join[last_join_table_no]["on"]["second_table_on"]),
                                                     TableTypes.DATA.value:
                                                     set(temp_join[0]["on"]["first_table_on"]),
                                                     }

            same_dimensions: bool = True

            dim_set_no: int = 0
            fact_tables_in_join = list(dimension_join_fields.keys())
            while dim_set_no < len(fact_tables_in_join) - 1:

                current_fact_table = fact_tables_in_join[dim_set_no]
                next_fact_table = fact_tables_in_join[dim_set_no + 1]

                if (len(dimension_join_fields[current_fact_table][TableTypes.DIMENSION.value]) !=
                        len(dimension_join_fields[next_fact_table][TableTypes.DIMENSION.value])):
                    same_dimensions = False
                    break

                for item in dimension_join_fields[current_fact_table][TableTypes.DIMENSION.value]:
                    if item not in dimension_join_fields[next_fact_table][TableTypes.DIMENSION.value]:
                        same_dimensions = False
                        break

                dim_set_no += 1

            for fact_table in fact_tables_in_join:
                if same_dimensions:
                    # All fields in dimension tables are the same for joins for fact table
                    for field in dimension_join_fields[fact_table][TableTypes.DIMENSION.value]:
                        dimension_select.add_field(fact_table, field.split(".")[-1])

                    # This is for fact cte_i to be able to join with main cte
                    selected_objects[TableTypes.DIMENSION.value][dimension_table][FieldType.SELECT.value].update(
                        dimension_join_fields[fact_table][TableTypes.DIMENSION.value])

                if not same_dimensions:
                    # All fields in dimension tables are NOT the same for joins for fact table
                    dimension_select.update_field(fact_table, dimension_join_fields[fact_table][
                        TableTypes.DATA.value])

        # Start building CTEs
        # TODO: create special format
        cte_properties = {}

        cte_no = 0

        # Will contain data for cte
        cte_properties[self.ALL_CTE] = {}

        for fact_table in fact_tables:
            current_cte = self.CTE.format(cte_no)
            cte_properties[self.ALL_CTE][current_cte] = {}
            current_select = copy.deepcopy(selected_objects)
            current_select.remove_all_fact_tables_except_named(fact_table)
            cte_properties[self.ALL_CTE][current_cte][self.QUERY_K] = self.generate_select_for_one_data_table(
                current_select)
            cte_properties[self.ALL_CTE][current_cte][self.OUT_K] = set()

            # Fields to be joined with cte_m
            cte_properties[self.ALL_CTE][current_cte][self.CTE_JOIN] = dimension_select[fact_table]

            # TODO: SYNC this with BBBB
            for item in range(len(selected_objects[TableTypes.DATA.value][fact_table][
                                      self.CALCULATIONS_K])):
                cte_properties[self.ALL_CTE][current_cte][self.OUT_K].add(self.CALC_FIELD.format(fact_table.split(
                    ".")[-1], item))

            cte_no += 1

        cte_properties["calculations"] = set()
        cte_properties[self.DIMENSION_SELECTS_K] = set()

        for dimension_table in dimension_tables:
            cte_properties[self.DIMENSION_SELECTS_K].update(
                selected_objects[TableTypes.DIMENSION.value][dimension_table][
                    "select"])

        # Build all CTEs
        query = self.__generate_text_query_for_multiple_tables(cte_properties)

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
            calculation_select = "\n\t,"

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
            where_query += "\nand ".join(["({})".format(f) for f in where])
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

    def __generate_text_query_for_multiple_tables(self, cte_properties: dict) -> str:
        """
        Generates query text for multiple fact tables
        :param cte_properties: prepared for CTE tables dict
        :return: SQL query
        """
        query = "WITH \n"

        cte_template = "{} as \n(\n{}\n)"
        main_cte_query_full = ",\n" + str(self.MAIN_CTE) + " as \n({})"
        # Contains select statements for main_cte
        main_cte_table_queries: list[str] = []
        union_cte_query = "\nSELECT\n\t {} \nFROM {}"
        left_join_cte: list[str] = []
        left_join_template: str = "LEFT JOIN {}\n\tON\n\t{}"
        field_equality: str = "{}.{} = {}.{}"

        select_fields: list[str] = []
        select_field_template: str = "{}.{}"

        coalesce_template: str = "COALESCE({})"

        cte_query: list[str] = []

        # START generate code for CTEs

        for cte in cte_properties[self.ALL_CTE]:
            # Generates selects for main_cte
            main_cte_table_queries.append(union_cte_query.format("\n\t,".join(cte_properties[self.ALL_CTE][cte][
                                                                                  self.CTE_JOIN]), cte))
            cte_query.append(cte_template.format(cte, cte_properties[self.ALL_CTE][cte][self.QUERY_K]))
            and_join: list[str] = []

            for field in cte_properties[self.ALL_CTE][cte][self.CTE_JOIN]:
                and_join.append(field_equality.format(cte, field, self.MAIN_CTE, field))

            for field in cte_properties[self.ALL_CTE][cte][self.OUT_K]:
                select_fields.append(select_field_template.format(cte, field))

            left_join_cte.append(left_join_template.format(cte, "\n\tAND ".join(and_join)))

        for dimension_field in cte_properties[self.DIMENSION_SELECTS_K]:
            dimension_select_list: list[str] = []
            for cte in cte_properties[self.ALL_CTE]:
                dimension_select_list.append(select_field_template.format(cte, dimension_field.split(".")[-1]))
            select_fields.append(coalesce_template.format(", ".join(dimension_select_list)))

        query += ",\n".join(cte_query)
        query += main_cte_query_full.format("\nUNION".join(main_cte_table_queries))

        # END generate code for CTEs

        # START generate code for select
        select: str = "\n\t,".join(select_fields)
        query += union_cte_query.format(select, self.MAIN_CTE)
        query += "\n" + "\n".join(left_join_cte)

        return query
