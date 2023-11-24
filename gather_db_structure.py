from typing import Optional

import toml
import os
import warnings

FILTERS = r"db_structure\standard_filters"
JOINS = r"db_structure\joins"
TABLES = r"db_structure\tables"


def list_toml_files_in_directory(directory: str) -> list:
    """
    Returns list of all toml files in directory
    :param directory: directory with toml files
    :return: list of toml files found
    """
    all_files = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if (os.path.isfile(f)) and (f.split(".")[-1] == "toml"):
            all_files.append(f)

    if len(all_files) == 0:
        warnings.warn(f"Нужные файлы в папке {directory} не найдены")

    return all_files


def gather_data_from_toml_files_into_big_dictionary(list_of_files: list, check_for_duplicate_key: str,
                                                    mandatory_keys: Optional[list | None] = None, ) -> dict:
    """
    Gathers data from toml files and check for duplicates and mandatory fields
    :param list_of_files: list with paths to toml files
    :param check_for_duplicate_key: name of key to check for duplicates. So we would not have two same tables
    :param mandatory_keys: keys that toml file should contain
    :return: dictionary from all files
    """

    if mandatory_keys is None:
        mandatory_keys = []
    result: dict = {}

    for file in list_of_files:
        temp_toml: dict = toml.load(file)

        # TODO: Надо добавить бд и схему
        non_duplicate_key = temp_toml[check_for_duplicate_key]

        if non_duplicate_key in result:
            raise RepeatingTableException(file, non_duplicate_key, check_for_duplicate_key)

        for key in mandatory_keys:
            if key not in temp_toml:
                raise NoMandatoryKeyException(file, key)

        result[non_duplicate_key] = temp_toml

    return result


class TablesInfoLoader:
    """
    Tables loading class with all possible joins and filters
    """

    __tables_dict: dict = {}
    __joins_dict: dict = {}
    __filters_dict: dict = {}
    __joins_by_table: dict = {}

    def __init__(self, tables: str = TABLES, filters: str = FILTERS, joins: str = JOINS) -> None:
        """
        Gets data from all toml files
        Checks for duplicates and other errors
        :param tables: folder, containing tables
        :param filters: folder, containing filters
        :param joins: folder, containing joins
        """
        self.current_path: str = os.path.abspath(os.getcwd())

        list_of_tables = list_toml_files_in_directory(os.path.join(self.current_path, tables))
        list_of_filters = list_toml_files_in_directory(os.path.join(self.current_path, filters))
        list_of_joins = list_toml_files_in_directory(os.path.join(self.current_path, joins))

        # TODO: Add mandatory fields
        self.__tables_dict = gather_data_from_toml_files_into_big_dictionary(list_of_tables, "table")
        self.__joins_dict = gather_data_from_toml_files_into_big_dictionary(list_of_joins, "first_table", )
        self.__filters_dict = gather_data_from_toml_files_into_big_dictionary(list_of_filters, "filter_name")

        self.__redistribute_joins_by_table()

    def check_tables_dict(self):
        # TODO: write check for tree-fields
        pass

    def check_filters(self):
        # TODO: check all filters
        pass

    def check_joins(self):
        # TODO: write check joins
        pass

    def __redistribute_joins_by_table_and_generate_all_fields(self) -> None:
        """
        Creates structure to make queries fast
        Groups all tables by it type of join with structure
        {
        left:
            {table_name:
                {tables right to table name: join_on }
            },

        right...
        }
        :return:
        """

        # TODO: generate all fields list

        self.__joins_by_table["left"] = {}
        self.__joins_by_table["right"] = {}
        self.__joins_by_table["inner"] = {}

        for name in self.__joins_dict:

            table_first_complete_name = "{}.{}.{}".format(self.__joins_dict[name]["database"],
                                                          self.__joins_dict[name]["schema"],
                                                          self.__joins_dict[name]["first_table"])

            for join_field in self.__joins_dict[name]["second_table"]:
                table_second_complete_name = "{}.{}.{}".format(self.__joins_dict[name]["database"],
                                                               self.__joins_dict[name]["schema"],
                                                               join_field)

                on_generation = self.__joins_dict[name]["second_table"][join_field]["on"]

                how = self.__joins_dict[name]["second_table"][join_field]["how"]

                if table_first_complete_name not in self.__joins_by_table[how]:
                    self.__joins_by_table[how][table_first_complete_name] = {}
                self.__joins_by_table[how][table_first_complete_name][table_second_complete_name] = \
                    on_generation

    def get_tables_dictionary(self) -> dict:
        return self.__tables_dict

    def get_joins_dictionary(self) -> dict:
        """Returns joins with dictionary"""
        return self.__joins_dict

    def get_joins_by_table_dictionary(self) -> dict:
        """Returns dictionary with tables and their properties"""
        return self.__joins_by_table

    def get_filters_dictionary(self) -> dict:
        """Returns dictionary with filters"""
        return self.__filters_dict


class RepeatingTableException(Exception):
    """
    Error is thrown where we got two or more objects with repeating names
    """

    def __init__(self, file_name: str, name: str, duplicate_key_name: str) -> None:
        message = f"В файле {file_name} обнаружен дубликат {duplicate_key_name} {name}"
        super().__init__(message)


class NoMandatoryKeyException(Exception):
    def __init__(self, file_name: str, key: str) -> None:
        message = f"В файле {file_name} не найден ключ {key}"
        super().__init__(message)


if __name__ == "__main__":
    c = TablesInfoLoader()
    print(c.get_joins_by_table_dictionary())
