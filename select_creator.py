from custom_data_types import FieldsFromFrontend
from shortest_joins import ShortestDistance


class SelectCreator:
    def __init__(self, tables_dict: dict):
        self.tables_dict = tables_dict
        self.joins: ShortestDistance = ShortestDistance()

    def count_data_tables(self) -> int:
        """
        Count how many fact tables in query
        If we have more than one query, we have to work with CTE
        :return:
        """
        pass

    def create_query(self, selected_objects: FieldsFromFrontend) -> str:
        pass


class SelectPostgres(SelectCreator):
    def count_data_tables(self) -> int:
        all_tables = set()
        return 0

