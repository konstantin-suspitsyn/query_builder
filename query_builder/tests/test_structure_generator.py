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
        Should check than Warning is thrown for empty directore
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
        self.assertEqual(len(all_tables.keys()), len(os.listdir(tables_folder_link)))

        # Test table types
        correct_table_types = True
        all_table_types = [t.value for t in TableTypes]
        for table in all_tables:
            if all_tables[table] not in all_table_types:
                correct_table_types = False

        self.assertTrue(correct_table_types)


if __name__ == "__main__":
    unittest.main()
