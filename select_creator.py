import copy

from custom_data_types import FieldsForQuery
from enum_query_builder import TomlTableTableTypeFieldPossibleValues
from shortest_joins import ShortestDistance
from utilities_query_builder import join_on_to_string, where_to_fields




class SelectCreator:
    CTE = "cte_{}"
    MAIN_JOIN_TABLE = "query_builder.public.dim_calendar"
    CALC_FIELD = "{}_calc_{}"

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
            calculation_list = []
            i = 0
            for c in calculation:
                calculation_list.append("{} as {}".format(c, self.CALC_FIELD.format(from_table.split(".")[-1], i)))
                i += 1
            query += "\n," + "\n,".join(calculation_list)

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

    def select_for_multiple_fact_tables(self, selected_objects: FieldsForQuery) -> str:

        dimension_tables = selected_objects.get_dimension_tables()
        fact_tables = selected_objects.get_fact_tables()
        all_tables = selected_objects.get_all_tables()

        # Fast check if all joins exist
        for fact_table in fact_tables:
            if len(selected_objects[TomlTableTableTypeFieldPossibleValues.DATA.value][fact_table]["select"]) > 0:
                raise RuntimeError("Select on fact join")

            for dimension_table in dimension_tables:

                if not self.joins.has_join(fact_table, dimension_table):
                    raise RuntimeError("No join")

        main_query = "select\n"
        from_query = "from {} \n"
        join_template = """left join ({}) as  {} 
            on {}"""

        cte_properties = {}

        cte_no = 0
        dimension_select = set()
        for fact_table in fact_tables:
            cte_properties[self.CTE.format(cte_no)] = {}
            current_select = copy.deepcopy(selected_objects)
            current_select.remove_all_fact_tables_except_named(fact_table)
            cte_properties[self.CTE.format(cte_no)]["query"] = self.select_for_one_table(current_select)
            cte_properties[self.CTE.format(cte_no)]["out"] = set()

            for item in range(len(selected_objects[TomlTableTableTypeFieldPossibleValues.DATA.value][fact_table][
                                      "calculations"])):
                cte_properties[self.CTE.format(cte_no)]["out"].add(self.CALC_FIELD.format(fact_table.split(".")[
                                                                                              -1], item))

            cte_no += 1

        # Main CTE fields
        for dimension_table in dimension_tables:
            for item in selected_objects[TomlTableTableTypeFieldPossibleValues.DIMENSION.value][dimension_table][
                    "select"]:
                print(item.split(".")[-1])
                dimension_select.add(item.split(".")[-1])

        cte_template = "{} as ({})\n"

        main_cte: list[str] = []
        main_cte_name = "cte_m"
        other_cte: list[str] = []
        for cte in cte_properties:
            main_cte.append("select\n{}\nfrom {}".format("\n,".join(dimension_select), cte))
            other_cte.append(cte_template.format(cte, cte_properties[cte]["query"]))

        the_select = "\nselect\n"

        big_select = "with\n"
        big_select += "\n, \n".join(other_cte)
        big_select += "\n," + cte_template.format(main_cte_name, "\nunion\n".join(main_cte))

        the_select += ",\n".join(["{}.{}".format(main_cte_name, f) for f in dimension_select])

        for cte in cte_properties:
            the_select += ",\n"
            the_select += ",\n".join(["{}.{}".format(cte, f) for f in cte_properties[cte]["out"]])

        the_select += "\nfrom {}\n".format(main_cte_name)

        the_select += "\n"

        for cte in cte_properties:
            the_select += "\nleft join {}\n".format(cte)
            the_select += "ON "
            for dimension in dimension_select:
                the_select += "{}.{} = {}.{} AND".format(cte, dimension, main_cte_name, dimension)

            the_select = the_select[:-4]

        big_select += the_select

        return big_select

    @staticmethod
    def check_if_all_tables_in_list(list_of_tables_from: list | set, list_of_tables_to: list | set) -> bool:
        for item in list_of_tables_from:
            if item not in list_of_tables_to:
                return False
        return True
