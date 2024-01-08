from typing import Tuple

from custom_data_types import FieldsForQuery, FieldsFromFrontend
from enum_query_builder import TomlTableTableTypeFieldPossibleValues, TomlPossibleFieldKeywordsForTable, \
    TomlTableCalculationFieldProperties
from exceptions_query_builder import UnknownTableFieldProperty
from gather_db_structure import TablesInfoLoader
from utilities_query_builder import get_table_from_field, split_to_fields, split_where_string_to_fields


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

    def get_all_fields_for_query_and_sort(self, fields_for_query_structure: FieldsFromFrontend) -> FieldsForQuery:
        """
        Gets all fields for query and sort them by types od tables, fields and filters
        :param fields_for_query_structure: dictionary with fields from frontend
            {
                "select": [list of fields to select, ...],
                "calculations": [list of calculations],
                "where": {field: string with condition,...}
            }
        :return: dictionary with
            {
                "fact":
                    {
                        fact_table_1:
                            {
                                "select": set of fields,
                                "calculations": set of calculated fields,
                                "where": set of strings with conditions,
                                "not_for_select": set of fields
                            },
                        fact_table_2...
                    }
                "dimension":
                    {
                        dimension_table_1:
                            {
                                "select": set of fields,
                                "calculations": set of calculated fields,
                                "where": {field: "condition"},
                                "not_for_select": set of fields
                            },
                        dimension_table_2...
                    },

                "where": [list of conditions for all data]
            }
         structure
        """

        # Generate all possible table types
        all_fields_by_table = FieldsForQuery()

        def create_table_structure() -> dict:
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

        def create_table_if_not_exists(current_field: str) -> Tuple[str, str]:
            """
            Adds structure for non-existing tables
            :param current_field:
            :return: current_table_type, current_table
            """
            current_function_table = get_table_from_field(current_field)
            current_function_table_type = self.dict_table[current_function_table]

            if current_function_table not in all_fields_by_table[current_function_table_type]:
                all_fields_by_table[current_function_table_type][current_function_table] = create_table_structure()

            return current_function_table_type, current_function_table

        def get_all_fields_from_calculation(calculation_formula: str) -> dict:
            """
            Returns all tables by type
            :param calculation_formula:
            :return: {"table_type": set of field names}
            """

            tables_from_calculation = dict()
            for f_current_table_type in TomlTableTableTypeFieldPossibleValues:
                tables_from_calculation[f_current_table_type.value] = set()

            list_of_fields = split_to_fields(calculation_formula, None)
            for current_field in list_of_fields:
                _table_type = self.dict_table[get_table_from_field(current_field)]
                tables_from_calculation[_table_type].add(current_field)

            return tables_from_calculation

        def calculated_field_to_structure(field_f: str, current_table_name: str,
                                          current_table_function_type: str) -> None:
            """
            Worker for any type of calculated fields
            :param field_f:
            :param current_table_function_type:
            :param current_table_name: current table name
            :return:
            """
            current_calculated_field = self.dict_fields[field_f]["calculation"]

            list_of_fields = split_to_fields(current_calculated_field, current_table_name)

            for calculated_field in list_of_fields:
                # Add all tables to join later
                all_fields_by_table[current_table_function_type][current_table_name]["join_tables"].add(
                    get_table_from_field(calculated_field))

            all_fields_by_table[current_table_function_type][current_table_name]["calculations"].add(
                current_calculated_field)
            all_fields_by_table[current_table_function_type][current_table_name]["where"].add(self.dict_fields[
                field_f][TomlTableCalculationFieldProperties.WHERE.value])
            all_fields_by_table[current_table_function_type][current_table_name]["fact_must_join_on"].update(
                self.dict_fields[field_f][TomlTableCalculationFieldProperties.FACT_MUST_JOIN_ON.value])
            all_fields_by_table[current_table_function_type][current_table_name]["no_join_fact"].update(
                self.dict_fields[field_f][TomlTableCalculationFieldProperties.NO_JOIN_FACT.value])

        for field in fields_for_query_structure["select"]:
            current_table_type, current_table = create_table_if_not_exists(field)

            # There are two types of fields. Simple select and pre-calculated select
            # Simple select field (select or value)
            if (self.dict_fields[field]["type"] == TomlPossibleFieldKeywordsForTable.TYPE_SELECT.value) \
                    or (self.dict_fields[field]["type"] == TomlPossibleFieldKeywordsForTable.TYPE_VALUE.value):
                all_fields_by_table[current_table_type][current_table]["select"].add(field)

            # Calculation type
            elif self.dict_fields[field]["type"] == TomlPossibleFieldKeywordsForTable.TYPE_CALCULATION.value:
                calculated_field_to_structure(field, current_table, current_table_type)
            else:
                raise UnknownTableFieldProperty(current_table, field, self.dict_fields[field])

        for field in fields_for_query_structure["calculations"]:
            tables_in_calculation = get_all_fields_from_calculation(field)
            if len(tables_in_calculation[TomlTableTableTypeFieldPossibleValues.DATA.value]) > 0:
                current_table_type, current_table = create_table_if_not_exists(
                    tables_in_calculation[TomlTableTableTypeFieldPossibleValues.DATA.value][0])

                for non_act_table in tables_in_calculation[TomlTableTableTypeFieldPossibleValues.DIMENSION.value]:
                    all_fields_by_table[current_table_type][current_table]["not_for_select"].add(non_act_table)

        all_fields_by_table["where"] = fields_for_query_structure["where"]
        for field in split_where_string_to_fields(fields_for_query_structure["where"], self.dict_fields):
            current_table_type, current_table = create_table_if_not_exists(field)

            # Adding to not for select only if we don't have it in select directly
            if field not in all_fields_by_table[current_table_type][current_table]["select"]:
                all_fields_by_table[current_table_type][current_table]["not_for_select"].add(field)

        return all_fields_by_table


if __name__ == "__main__":
    tables_info_loader = TablesInfoLoader()
    join_dict = tables_info_loader.get_joins_by_table_dictionary()
