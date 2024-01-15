from typing import Tuple

from query_builder.utils.data_types import FieldsFromFrontend, FieldsForQuery
from query_builder.utils.enums_and_field_dicts import FieldType, TableTypes, FrontendTypeFields
from query_builder.utils.utils import get_table_from_field, get_fields


class FrontendBackendConverter:
    """
    Converts data from frontend to backend for further query creation
    """

    def __init__(self, dict_fields: dict, dict_table: dict) -> None:
        """
        Initialize class
        :param dict_fields: all fields with properties
        :param dict_table: dict with table and properties
        """
        self.dict_fields = dict_fields
        self.dict_table = dict_table

    def convert_from_frontend_to_backend(self, fields_for_query_structure: FieldsFromFrontend) -> FieldsForQuery:
        """
        Receives data from frontend as type of FieldsFromFrontend and converts it to FieldsForQuery type
        :param fields_for_query_structure:
        :return:
        """

        # Generate all possible table types
        all_fields_by_table = FieldsForQuery()

        # Working with select
        for frontend_field_type in fields_for_query_structure:
            # Could be one of [select, where, calculations]
            for field in fields_for_query_structure[frontend_field_type]:
                current_table: str
                current_table_type: str

                select: set = set()
                calculations: set = set()
                where: set = set()
                join_tables: set = set()

                if frontend_field_type == FrontendTypeFields.SELECT.value:
                    current_table = get_table_from_field(field)
                    current_table_type = self.dict_table[current_table]
                    field_type = self.dict_fields[field]
                    if field_type == FieldType.CALCULATION.value:
                        calculations.add(self.dict_fields[field]["calculation"])
                        if "where" in self.dict_fields[field]:
                            where.add(self.dict_fields[field]["where"])
                        if "join_tables" in self.dict_fields[field]:
                            join_tables.add(self.dict_fields[field]["join_tables"])

                    if field_type in [FieldType.SELECT.value, FieldType.VALUE.value]:
                        select.add(field)

                    all_fields_by_table.add_fields_to_table(table_name=current_table,
                                                            table_type=current_table_type,
                                                            select=select,
                                                            calculations=calculations,
                                                            where=where,
                                                            join_tables=join_tables)

                if frontend_field_type in [FrontendTypeFields.CALCULATIONS.value, FrontendTypeFields.WHERE.value]:
                    data_tables, dimension_tables = self.__get_tables(field)
                    if frontend_field_type == FrontendTypeFields.CALCULATIONS.value:
                        calculations.add(field)
                    if frontend_field_type == FrontendTypeFields.WHERE.value:
                        where.add(field)

                    current_table: str = ""
                    # Do not change order of len ifs
                    if len(data_tables) == 0:
                        current_table = dimension_tables.pop()

                    if len(data_tables) == 1:
                        current_table = data_tables.pop()

                    # TODO: think of something with two data tables in one calculation
                    if len(data_tables) > 1:
                        raise RuntimeError("This was not yet planned")

                    current_table_type = self.dict_table[current_table]

                    all_fields_by_table.add_fields_to_table(table_name=current_table,
                                                            table_type=current_table_type,
                                                            select=select,
                                                            calculations=calculations,
                                                            where=where,
                                                            join_tables=join_tables)

                    for dimension_table in dimension_tables:
                        all_fields_by_table.add_table_if_not_exist(dimension_table, "dimension")

        return all_fields_by_table

    def __get_tables(self, aggregation_or_where: str) -> Tuple[set, set]:
        """
        Returns data_tables and dimension_tables from aggregation or where clause
        :param aggregation_or_where:
        :return:
        """
        data_tables = set()
        dimension_tables = set()

        extracted_fields = get_fields(aggregation_or_where)

        for field in extracted_fields:
            if field not in self.dict_fields:
                continue

            table_from_field = get_table_from_field(field)

            if self.dict_table[table_from_field] == TableTypes.DATA.value:
                data_tables.add(table_from_field)

            if self.dict_table[table_from_field] == TableTypes.DIMENSION.value:
                dimension_tables.add(table_from_field)

        return data_tables, dimension_tables
