from gather_db_structure import TablesInfoLoader
from pre_query_builder import PreQueryBuilder

one_table_from_front = {
    "select": [
        "query_builder.public.fact_stock.value",
        "query_builder.public.dim_item.name"
               ],
    "where": "query_builder.public.dim_calendar.date = '2023-01-01'"
}

two_tables_from_front = {
    "select": [
        "query_builder.public.fact_stock.value",
        "query_builder.public.dim_item.name",
        "query_builder.public.fact_stock.last_day_of_week_pcs",
        "query_builder.public.fact_sales.value",
               ],
    "calculations": [
        "sum(query_builder.public.fact_stock.value * query_builder.public.dim_item.price)"
    ],
    "where": "query_builder.public.dim_calendar.date = '2023-01-01'"
}

if __name__ == "__main__":
    db = TablesInfoLoader()
    fields = db.get_all_fields()
    tables = db.get_all_tables()
    pqb = PreQueryBuilder(fields, tables)
    query_and_sort = pqb.get_all_fields_for_query_and_sort(two_tables_from_front)
    print(query_and_sort)
