from utilities_query_builder import split_where_string_to_fields

if __name__ == "__main__":
    a = {}
    a["query_builder.public.fact_stock.value"] = 1
    a["query_builder.public.item.price"] = 1

    print(split_where_string_to_fields("sum(query_builder.public.fact_stock.value * query_builder.public.item.price)", a))

    b = set()
    b.add("a")
    b.add("b")

    print(b)
