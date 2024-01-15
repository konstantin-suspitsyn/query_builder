import unittest

from query_builder.utils.utils import get_table_from_field, get_field_name_only, get_fields


class TestUtils(unittest.TestCase):

    def test_get_table_from_field(self):
        """
        Should return name of table
        :return:
        """

        field_name = "qwerty.asdfg.zxcvb"

        table_name = get_table_from_field(field_name)

        self.assertEqual("qwerty.asdfg", table_name)

    def test_get_field_name_only(self):
        field_name = "qwerty.asdfg.zxcvb"

        short_field_name = get_field_name_only(field_name)

        self.assertEqual("zxcvb", short_field_name)

    def test_get_fields(self):
        test_string = "sum(query_builder.public.fact_stock.value * query_builder.public.dim_item.price)"
        get_sum = get_fields(test_string)

        found_all_fields: bool = True

        should_get_fields = set()
        should_get_fields.update(["query_builder.public.fact_stock.value", "query_builder.public.dim_item.price"])

        for item in get_sum:
            if item not in should_get_fields:
                found_all_fields = False

        self.assertTrue(found_all_fields)


if __name__ == "__main__":
    unittest.main()
