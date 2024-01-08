from custom_data_types import FieldsFromFrontend
from dijkstra import DijkstraJoins
from gather_db_structure import TablesInfoLoader
from pre_query_builder import PreQueryBuilder
from select_creator import SelectPostgres
from shortest_joins import ShortestDistance

one_table_from_front = FieldsFromFrontend({
    "select": [
        "query_builder.public.fact_stock.first_day_of_week_pcs",
        "query_builder.public.fact_stock.date",
        "query_builder.public.dim_item.name",

               ],
    "where": "query_builder.public.dim_calendar.date = '2023-01-01'"
})

two_tables_from_front = FieldsFromFrontend({
    "select": [
        "query_builder.public.dim_item.name",
        "query_builder.public.fact_stock.last_day_of_week_pcs",
        "query_builder.public.fact_sales.value",
               ],
    "calculations": [
        "sum(query_builder.public.fact_stock.value * query_builder.public.dim_item.price)"
    ],
    "where": "query_builder.public.dim_calendar.date = '2023-01-01'"
})

if __name__ == "__main__":
    db = TablesInfoLoader()
    fields = db.get_all_fields()
    tables = db.get_all_tables()
    pqb = PreQueryBuilder(fields, tables)
    query_and_sort = pqb.get_all_fields_for_query_and_sort(two_tables_from_front)
    print(query_and_sort)

    direct_joins_ = db.get_joins_by_table_dictionary()
    dijkstra_joins = DijkstraJoins(direct_joins_, tables)

    sj = ShortestDistance()

    sc = SelectPostgres(tables)
    print(sc.create_query(query_and_sort))
    sc.create_query(query_and_sort)
