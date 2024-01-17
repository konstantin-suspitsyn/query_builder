import unittest

from query_builder.universe.joins_generator import GenerateJoins
from query_builder.universe.possible_joins import AllPossibleJoins
from query_builder.universe.structure_generator import StructureGenerator


class TestJoins(unittest.TestCase):
    """
    Test for AllPossibleJoins class
    """

    def test_generate_all_joins(self):
        table_structure = StructureGenerator(
            r"./../tests/test_db_structure/test_tables",
            r"./../tests/test_db_structure/test_joins",
            r"./../tests/test_db_structure/test_standard_filters",
        )
        GenerateJoins(table_structure.get_joins(), table_structure.get_tables())
        possible_joins = AllPossibleJoins()
        joins = possible_joins.get_all_joins()
        print(joins)
