from query_builder.utils.utils import singleton


@singleton
class AllPossibleJoins:
    __short_distance = {}

    def has_join(self, start_table: str, end_table: str) -> bool:
        """
        Checks if self.__short_distance has join between tables start_table and end_table
        :param start_table:
        :param end_table:
        :return:
        """
        if start_table not in self.__short_distance:
            return False

        if end_table not in self.__short_distance[start_table]:
            return False

        return True

    def has_table_with_joins(self, start_table: str) -> bool:
        """
        Checks if self.__short_distance has join starting with start_table
        :param start_table:
        :return:
        """
        if start_table not in self.__short_distance:
            return False

        return True

    def all_joins_by_starting_table(self, join_dict: dict):
        self.__short_distance.update(join_dict)

    def add_join(self, start_table: str, end_table: str, complete_path_of_joins: dict) -> None:
        """
        Adds join to self.__short_distance
        :param start_table:
        :param end_table:
        :param complete_path_of_joins:
        :return:
        """
        if not self.has_join(start_table, end_table):
            self.__short_distance[start_table] = {}
            self.__short_distance[start_table][end_table] = complete_path_of_joins

    def get_join(self, start_table: str, end_table: str) -> dict | bool:
        """
        Returns a join
        :param start_table:
        :param end_table:
        :return:
        """
        if not self.has_join(start_table, end_table):
            return False
        return self.__short_distance[start_table][end_table]

    def get_all_joins(self) -> dict:
        """
        Return all joins that were created
        :return:
        """
        return self.__short_distance
