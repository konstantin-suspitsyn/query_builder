import unittest

from query_builder.universe.frontend_backend_converter import FrontendBackendConverter
from query_builder.universe.joins_generator import GenerateJoins
from query_builder.universe.possible_joins import AllPossibleJoins
from query_builder.universe.query_generator import QueryGenerator
from query_builder.universe.structure_generator import StructureGenerator
from query_builder.utils.data_types import FieldsFromFrontend


class TestQueryGenerator(unittest.TestCase):
    def test_convert_from_frontend_to_backend(self):
        table_structure = StructureGenerator(
            r"./../tests/test_db_structure/test_tables",
            r"./../tests/test_db_structure/test_joins",
            r"./../tests/test_db_structure/test_standard_filters",
        )

        one_table_from_front = FieldsFromFrontend({
            "select": [
                "query_builder.public.fact_stock.first_day_of_week_pcs",
                "query_builder.public.dim_calendar.date",
                "query_builder.public.dim_item.name",

            ],
            "where": ["query_builder.public.dim_calendar.date = '2023-01-01'"]
        })

        front_to_back = FrontendBackendConverter(table_structure.get_fields(), table_structure.get_tables())
        fields_rebuild = front_to_back.convert_from_frontend_to_backend(one_table_from_front)
        query_generator = QueryGenerator(table_structure.get_tables())
        GenerateJoins(table_structure.get_joins(), table_structure.get_tables())
        possible_joins = AllPossibleJoins()
        print(query_generator.generate_select_for_one_data_table(fields_rebuild))

    def test_convert_from_frontend_to_backend_two_tables(self):
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
        query_generator = QueryGenerator(table_structure.get_tables())
        GenerateJoins(table_structure.get_joins(), table_structure.get_tables())
        possible_joins = AllPossibleJoins()
        print(query_generator.generate_select_for_multiple_data_tables(fields_rebuild))

    def test_convert_from_frontend_to_backend_one_table(self):
        table_structure = StructureGenerator(
            r"./../tests/test_db_structure/test_tele_tables",
            r"./../tests/test_db_structure/test_tele_joins",
            r"./../tests/test_db_structure/test_standard_filters",
        )

        two_tables_from_front = FieldsFromFrontend({
            "select": [
                "query_builder.public.dim_calendar.date",
                "abc.abc.dim_account_bud.bk_account_bud",
            ],
            "calculations": [
                "sum(abc.abc.hyperion.value)"
            ],
            "where": ["query_builder.public.dim_calendar.date = '2023-01-01'"]
        })

        front_to_back = FrontendBackendConverter(table_structure.get_fields(), table_structure.get_tables())
        fields_rebuild = front_to_back.convert_from_frontend_to_backend(two_tables_from_front)
        query_generator = QueryGenerator(table_structure.get_tables())
        GenerateJoins(table_structure.get_joins(), table_structure.get_tables())
        possible_joins = AllPossibleJoins()
        print(query_generator.generate_select_for_one_data_table(fields_rebuild))
