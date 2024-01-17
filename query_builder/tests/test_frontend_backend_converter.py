import unittest

from query_builder.universe.frontend_backend_converter import FrontendBackendConverter
from query_builder.universe.structure_generator import StructureGenerator
from query_builder.utils.data_types import FieldsFromFrontend


class TestFrontendBackendConverter(unittest.TestCase):
    def test_convert_from_frontend_to_backend(self):
        table_structure = StructureGenerator(
            r"./../tests/test_db_structure/test_tables",
            r"./../tests/test_db_structure/test_joins",
            r"./../tests/test_db_structure/test_standard_filters",
        )

        two_tables_from_front = FieldsFromFrontend({
            "select": [
                "query_builder.public.dim_item.name",
                "query_builder.public.fact_stock.last_day_of_week_pcs",
                "query_builder.public.dim_calendar.date",
            ],
            "calculations": [
                "sum(query_builder.public.fact_stock.value * query_builder.public.dim_item.price)",
                "sum(query_builder.public.fact_sales.value)",
            ],
            "where": ["query_builder.public.dim_calendar.date = '2023-01-01'"]
        })

        front_to_back = FrontendBackendConverter(table_structure.get_fields(), table_structure.get_tables())
        fields_rebuild = front_to_back.convert_from_frontend_to_backend(two_tables_from_front)

        answer = {'data': {'query_builder.public.fact_stock': {'select': set(), 'calculations': {
            'sum(query_builder.public.fact_stock.value * query_builder.public.dim_item.price)',
            'sum(query_builder.public.fact_stock.value)'}, 'where': {
            'query_builder.public.dim_calendar.last_day_of_week = 1'}, 'not_for_select': set(), 'join_tables': set(),
                                                               'fact_must_join_on': set(), 'no_join_fact': set()},
                           'query_builder.public.fact_sales': {'select': set(), 'calculations': {
                               'sum(query_builder.public.fact_sales.value)'}, 'where': set(), 'not_for_select': set(),
                                                               'join_tables': set(), 'fact_must_join_on': set(),
                                                               'no_join_fact': set()}}, 'dimension': {
            'query_builder.public.dim_item': {'select': {'query_builder.public.dim_item.name'}, 'calculations': set(),
                                              'where': set(), 'not_for_select': set(), 'join_tables': set(),
                                              'fact_must_join_on': set(), 'no_join_fact': set()},
            'query_builder.public.dim_calendar': {'select': {'query_builder.public.dim_calendar.date'},
                                                  'calculations': set(),
                                                  'where': {"query_builder.public.dim_calendar.date = '2023-01-01'"},
                                                  'not_for_select': set(), 'join_tables': set(),
                                                  'fact_must_join_on': set(), 'no_join_fact': set()}}}

        for key in answer.keys():
            self.assertTrue(key in fields_rebuild.keys())

        # Check_data
        for key in answer["data"].keys():
            self.assertTrue(key in fields_rebuild["data"].keys())

        # Check_dimension
        for key in answer["dimension"].keys():
            self.assertTrue(key in fields_rebuild["dimension"].keys())

        # Check_max_level
        for key_data_dim in answer.keys():
            for key_table_name in answer[key_data_dim].keys():
                for key_type_of_data in answer[key_data_dim][key_table_name].keys():
                    for set_item in answer[key_data_dim][key_table_name][key_type_of_data]:
                        self.assertTrue(set_item in answer[key_data_dim][key_table_name][key_type_of_data])

    def test_convert_from_frontend_to_backend_multi_where(self):
        table_structure = StructureGenerator(
            r"./../tests/test_db_structure/test_tables",
            r"./../tests/test_db_structure/test_joins",
            r"./../tests/test_db_structure/test_standard_filters",
        )

        two_tables_from_front = FieldsFromFrontend({
            "select": [
                "query_builder.public.dim_item.name",
                "query_builder.public.fact_stock.last_day_of_week_pcs",
                "query_builder.public.dim_calendar.date",
            ],
            "calculations": [
                "sum(query_builder.public.fact_stock.value * query_builder.public.dim_item.price)",
                "sum(query_builder.public.fact_sales.value)",
            ],
            "where": ["query_builder.public.dim_calendar.date = '2023-01-01' "
                      "and query_builder.public.dim_item.id = 123"]
        })

        front_to_back = FrontendBackendConverter(table_structure.get_fields(), table_structure.get_tables())
        fields_rebuild = front_to_back.convert_from_frontend_to_backend(two_tables_from_front)
        print(fields_rebuild)
