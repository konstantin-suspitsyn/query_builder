import unittest

from query_builder.universe.frontend_backend_converter import FrontendBackendConverter
from query_builder.universe.structure_generator import StructureGenerator
from query_builder.utils.data_types import FieldsFromFrontend


class TestFrontendBackendConverter(unittest.TestCase):
    def test_convert_from_frontend_to_backend(self):
        table_structure = StructureGenerator(
            r"../../db_structure/tables",
            r"../../db_structure/joins",
            r"../../db_structure/standard_filters",
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

        front_to_back = FrontendBackendConverter(table_structure.get_fields(), table_structure.get_all_tables())
        print(front_to_back.convert_from_frontend_to_backend(two_tables_from_front))
