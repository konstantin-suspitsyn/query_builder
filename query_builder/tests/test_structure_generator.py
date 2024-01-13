import unittest
import os

from query_builder.universe.structure_generator import StructureGenerator
from query_builder.utils.enums_and_field_dicts import TableTypes
from query_builder.utils.exceptions import NoMandatoryKeyException


class TestStructureGenerator(unittest.TestCase):
    """
    Test StructureGenerator class
    """

    def test_init_throws_warning(self):
        """
        Should check than Warning is thrown for empty directory
        """
        with self.assertWarns(UserWarning):
            StructureGenerator(
                r"./test_db_structure/tables_test_structure_generator",
                r"./test_db_structure/joins_test_structure_generator",
                r"./test_db_structure/empty_directory",
            )

    def test_init_throws_mandatory_key_error(self):
        """
        Should throw an error for non-existing key
        """
        with self.assertRaises(NoMandatoryKeyException):
            StructureGenerator(
                r"./test_db_structure/tables_test_structure_generator_incorrect_table",
                r"./test_db_structure/joins_test_structure_generator",
                r"./test_db_structure/empty_directory",
            )

    def test_get_all_tables(self):
        """
        Tests for all tables
        """
        tables_folder_link = r"./test_db_structure/tables_test_structure_generator"
        sg = StructureGenerator(
            tables_folder_link,
            r"./test_db_structure/joins_test_structure_generator",
            r"./test_db_structure/empty_directory",
        )

        # Test amount of tables
        all_tables = sg.get_all_tables()

        number_of_files = len(os.listdir(tables_folder_link))
        number_of_tables = len(all_tables.keys())
        self.assertEqual(number_of_tables, number_of_files)

        # Test table types
        correct_table_types = True
        all_table_types = [t.value for t in TableTypes]
        for table in all_tables:
            if all_tables[table] not in all_table_types:
                correct_table_types = False

        self.assertTrue(correct_table_types)

    def test_all_joins(self):
        tables_folder_link = r"./test_db_structure/tables_test_structure_generator"
        joins_folder_link = r"./test_db_structure/joins_test_structure_generator"
        sg = StructureGenerator(
            tables_folder_link,
            joins_folder_link,
            r"./test_db_structure/empty_directory",
        )

        all_joins = sg.get_joins()

        self.assertEqual(len(all_joins.keys()), len(os.listdir(joins_folder_link)))

    def test_all_fields(self):
        tables_folder_link = r"./test_db_structure/tables_two_tables_check_fields"
        joins_folder_link = r"./test_db_structure/joins_test_structure_generator"
        sg = StructureGenerator(
            tables_folder_link,
            joins_folder_link,
            r"./test_db_structure/empty_directory",
        )

        all_fields = sg.get_fields()

        should_return_fields = {'query_builder.public.dim_item.id': {'name': None, 'show': False, 'type': 'select'},
                                'query_builder.public.dim_item.sk_item_id': {'name': None, 'show': False,
                                                                             'type': 'select'},
                                'query_builder.public.dim_item.name': {'name': 'Название товара', 'show': True,
                                                                       'type': 'select'},
                                'query_builder.public.dim_item.volume': {'name': 'Объем товара, м3', 'show': True,
                                                                         'type': 'select'},
                                'query_builder.public.dim_item.price': {'name': 'Цена товара, руб.', 'show': True,
                                                                        'type': 'select'},
                                'query_builder.public.fact_stock.id': {'name': None, 'show': False, 'type': 'select'},
                                'query_builder.public.fact_stock.sk_item_id': {'name': None, 'show': False,
                                                                               'type': 'select'},
                                'query_builder.public.fact_stock.sk_warehouse_id': {'name': None, 'show': False,
                                                                                    'type': 'select'},
                                'query_builder.public.fact_stock.value': {'name': 'Запасы. Кол-во шт.', 'show': True,
                                                                          'type': 'value'},
                                'query_builder.public.fact_stock.date': {'name': None, 'show': False, 'type': 'select'},
                                'last_day_of_week_pcs': {'name': 'Запасы на последний день недели, шт', 'show': True,
                                                         'type': 'calculation',
                                                         'where': 'query_builder.public.dim_calendar.last_day_of_week '
                                                                  '= 1',
                                                         'calculation': 'sum(query_builder.public.fact_stock.value)'},
                                'first_day_of_week_pcs': {'name': 'Запасы на первый день недели, шт', 'show': True,
                                                          'type': 'calculation',
                                                          'where': 'query_builder.public.dim_calendar'
                                                                   '.first_day_of_week = 1',
                                                          'calculation': 'sum(query_builder.public.fact_stock.value)'},
                                'last_day_of_week_rub': {'name': 'Запасы на последний день недели, руб', 'show': True,
                                                         'type': 'calculation',
                                                         'where': 'query_builder.public.dim_calendar.last_day_of_week '
                                                                  '= 1',
                                                         'calculation': 'sum(query_builder.public.fact_stock.value * '
                                                                        'query_builder.public.item.price)'},
                                'first_day_of_week_rub': {'name': 'Запасы на последний день недели, руб', 'show': True,
                                                          'type': 'calculation',
                                                          'where': 'query_builder.public.dim_calendar'
                                                                   '.first_day_of_week = 1',
                                                          'calculation': 'sum(query_builder.public.fact_stock.value * '
                                                                         'query_builder.public.item.price)'}}

        keys_are_equal: bool = True
        all_fields_keys = set(all_fields.keys())
        should_return_fields_keys = set(should_return_fields.keys())

        self.assertEqual(len(all_fields_keys), len(should_return_fields_keys))

        for key in all_fields_keys:
            if key not in should_return_fields_keys:
                keys_are_equal = False

        self.assertTrue(keys_are_equal)


if __name__ == "__main__":
    unittest.main()
