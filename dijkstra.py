from gather_db_structure import TablesInfoLoader
from shortest_joins import ShortestDistance


class DijkstraJoins:
    all_tables = set()

    __join_weights = {"left": 2, "right": 3, "inner": 1}

    def __init__(self, direct_joins: dict, all_tables: dict) -> None:
        """
        :param direct_joins: direct joins are coming from TablesInfoLoader.class
        :param all_tables: all tables
        """
        # Singleton with shortest joins
        self.joins: ShortestDistance = ShortestDistance()
        self.direct_joins = direct_joins

        for table in all_tables:
            self.all_tables.add(table)

    def return_join(self, start_table: str, end_table: str) -> bool | dict:
        if not self.joins.has_join(start_table, end_table):
            self.best_joins_for_start(start_table)

        return self.joins.get_join(start_table, end_table)

    def best_joins_for_start(self, start_table: str) -> None:

        # Something like +∞ in Dijkstra algorithm
        max_no = 1e7
        min_node_count = 1e7
        min_node: str | None = None

        join_dict = {}
        joins_by_table = self.direct_joins.copy()

        all_tables = self.all_tables
        all_tables.remove(start_table)

        # Step 0. Create all connections
        for table in all_tables:

            join_dict[table] = {}
            if table in joins_by_table[start_table]:
                steps: int = self.__join_weights[joins_by_table[start_table][table]["how"]]
                join_dict[table]["steps"] = steps
                join_dict[table][0] = {}
                join_dict[table][0]["table"] = table
                for key in joins_by_table[start_table][table]:
                    join_dict[table][0][key] = joins_by_table[start_table][table][key]
                if (steps < min_node_count) & (table in joins_by_table):
                    min_node = table
                    min_node_count = steps
            else:
                join_dict[table]["steps"] = max_no

        # Remove visited connections
        del joins_by_table[start_table]

        j = self.recursive_joins(join_dict, joins_by_table, set(joins_by_table.keys()), min_node)

        print(j)

    def recursive_joins(self, created_joins: dict, all_joins: dict, all_tables: set, next_node: str | None) -> dict:
        if next_node is None:
            return created_joins

        all_tables.remove(next_node)

        for table in all_joins[next_node]:
            # Ignore existing nodes
            if table not in all_tables:
                continue
            steps: int = self.__join_weights[all_joins[next_node][table]["how"]]

            if created_joins[next_node]["steps"] + steps < created_joins[table]["steps"]:

                inner_dict_with_joins = created_joins[next_node].copy()

                all_keys = list(inner_dict_with_joins.keys())
                all_keys.remove("steps")

                next_key = max(all_keys) + 1
                inner_dict_with_joins[next_key] = {}
                inner_dict_with_joins[next_key]["table"] = table
                inner_dict_with_joins["steps"] = created_joins[next_node]["steps"] + steps
                for key in all_joins[next_node][table]:
                    inner_dict_with_joins[next_key][key] = all_joins[next_node][table][key]

                created_joins[table] = inner_dict_with_joins

        max_no = 1e7
        min_node: str | None = None

        for table in all_tables:
            if created_joins[table]["steps"] < max_no:
                max_no = created_joins[table]["steps"]
                min_node = table

        return self.recursive_joins(created_joins, all_joins, all_tables, min_node)


if __name__ == "__main__":
    table_info_loader = TablesInfoLoader()
    tables = table_info_loader.get_all_tables()
    direct_joins_ = table_info_loader.get_joins_by_table_dictionary()
    dijkstra_joins = DijkstraJoins(direct_joins_, tables)
    dijkstra_joins.best_joins_for_start("query_builder.public.fact_stock")
    dijkstra_joins.best_joins_for_start("query_builder.public.fact_sales")
