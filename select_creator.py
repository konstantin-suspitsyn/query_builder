from gather_db_structure import TablesInfoLoader
from shortest_joins import ShortestDistance


class SelectCreator:
    def __init__(self, tables_dict: dict, selected_objects: dict, all_possible_fields: dict):
        self.tables_dict = tables_dict
        self.selected_objects = selected_objects
        self.joins: ShortestDistance = ShortestDistance()
        self.all_possible_fields = all_possible_fields

    def count_data_tables(self) -> int:
        """
        Count how many fact tables in query
        If we have more than one query, we have to work with CTE
        :return:
        """
        pass


class SelectPostgres(SelectCreator):
    def count_data_tables(self) -> int:
        all_tables = set()
        return 0


if __name__ == "__main__":
    table_info_loader = TablesInfoLoader()
    tables = table_info_loader.get_all_tables()
    all_fields = table_info_loader.get_all_fields()
    sel_obj = {
        "select": ["query_builder.public.fact_stock.date", "query_builder.public.dim_item.name"],
        "calculation": ["sum(query_builder.public.fact_stock.value)"]
    }
    sp = SelectPostgres(tables, sel_obj, all_fields)
    sp.count_data_tables()
