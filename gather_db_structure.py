from typing import Union

import toml
import os
import warnings

from utilities_query_builder import split_to_fields

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


def true_false_converter(tf: str) -> bool:
    """
    Converter to return true or false from string
    :param tf: true of false string
    :return: True or False
    """
    if tf.lower() == "true":
        return True
    return False


def gather_data_from_toml_files_into_big_dictionary(list_of_files: list, check_for_duplicate_key: str,
                                                    mandatory_keys: Union[list | None] = None, ) -> dict:
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

        non_duplicate_key = temp_toml[check_for_duplicate_key]

        if non_duplicate_key in result:
            raise RepeatingTableException(file, non_duplicate_key, check_for_duplicate_key)

        for key in mandatory_keys:
            if key not in temp_toml:
                raise NoMandatoryKeyException(file, key)

        result[non_duplicate_key] = temp_toml

    return result


def always_return_list(input_data: Union[str, list]) -> list:
    """
    Checks if input data is a str and returns it as a list
    :param input_data: list or string
    :return: list
    """
    if isinstance(input_data, str):
        return [input_data]

    return input_data


class TablesInfoLoader:
    """
    Tables loading class with all possible joins and filters
    """

    __toml_tables_files_dict: dict = {}
    __joins_dict: dict = {}
    __filters_dict: dict = {}
    __joins_by_table: dict = {}
    __fields_dict: dict = {}
    __complete_dict_of_fields: dict = {}
    __short_tables_dictionary: dict = {}

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
        self.__toml_tables_files_dict = gather_data_from_toml_files_into_big_dictionary(list_of_tables, "table")
        self.__joins_dict = gather_data_from_toml_files_into_big_dictionary(list_of_joins, "first_table")
        self.__filters_dict = gather_data_from_toml_files_into_big_dictionary(list_of_filters, "filter_name")

        self.__redistribute_joins_by_table_and_generate_all_fields()
        self.__create_list_of_fields_and_short_dicts()

    def __create_list_of_fields_and_short_dicts(self) -> None:
        """
        Creates dictionary with all fields and it's properties
        :return: None
        """
        for file_name in self.__toml_tables_files_dict:

            table_name = self.__toml_tables_files_dict[file_name]["table"]
            schema_name = self.__toml_tables_files_dict[file_name]["schema"]
            database_name = self.__toml_tables_files_dict[file_name]["database"]
            table_full_name = "{}.{}.{}".format(database_name, schema_name, table_name)

            self.__short_tables_dictionary[table_full_name] = self.__toml_tables_files_dict[file_name]["table_type"]

            if "fields" in self.__toml_tables_files_dict[file_name]:
                for field_name in self.__toml_tables_files_dict[file_name]["fields"]:
                    self.__fill_in_field(database_name, field_name, "fields", file_name, schema_name, table_name)

            if "calculations" in self.__toml_tables_files_dict[file_name]:
                for field_name in self.__toml_tables_files_dict[file_name]["calculations"]:
                    self.__fill_in_field(database_name, field_name, "calculations", file_name, schema_name, table_name)

    def __fill_in_field(self, database_name: str, field_name: str, field_type: str, file_name: str, schema_name: str,
                        table_name: str) -> None:

        # TODO: DON'T really like this function
        """
        Helper method to fill in properties of field
        :param database_name:
        :param field_name:
        :param field_type:
        :param file_name:
        :param schema_name:
        :param table_name:
        :return:
        """
        complete_field_name = "{}.{}.{}.{}".format(database_name,
                                                   schema_name,
                                                   table_name,
                                                   field_name)
        self.__complete_dict_of_fields[complete_field_name] = {}
        self.__complete_dict_of_fields[complete_field_name]["type"] = self.__toml_tables_files_dict[file_name][
            field_type][field_name]["type"]
        self.__complete_dict_of_fields[complete_field_name]["show"] = \
            true_false_converter(self.__toml_tables_files_dict[file_name][field_type][field_name]["show"])
        if self.__complete_dict_of_fields[complete_field_name]["show"]:
            self.__complete_dict_of_fields[complete_field_name]["name"] = \
                self.__toml_tables_files_dict[file_name][field_type][field_name]["name"]

        # TODO: может надо отрефакторить
        if field_type == "calculations":
            calculation = self.__toml_tables_files_dict[file_name][field_type][field_name]["calculation"]
            self.__complete_dict_of_fields[complete_field_name]["calculation"] = calculation

            additional_fields = split_to_fields(calculation, "{}.{}.{}".format(database_name,
                                                                               schema_name,
                                                                               table_name))

            self.__complete_dict_of_fields[complete_field_name]["additional_fields"] = additional_fields
            self.__complete_dict_of_fields[complete_field_name]["where"] = \
                self.__toml_tables_files_dict[file_name][field_type][
                    field_name]["where"]

            self.__complete_dict_of_fields[complete_field_name]["fact_must_join_on"] = always_return_list(
                self.__toml_tables_files_dict[file_name][field_type][field_name]["fact_must_join_on"])

            self.__complete_dict_of_fields[complete_field_name]["no_join_fact"] = always_return_list(
                self.__toml_tables_files_dict[file_name][field_type][field_name]["no_join_fact"])

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
        table_name:
            {join_table:
                {"how": left/right/inner, "on" = string_on }
            },
        }
        :return:
        """

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

                if table_first_complete_name not in self.__joins_by_table:
                    self.__joins_by_table[table_first_complete_name] = {}
                self.__joins_by_table[table_first_complete_name][table_second_complete_name] = {}
                self.__joins_by_table[table_first_complete_name][table_second_complete_name]["how"] = how
                self.__joins_by_table[table_first_complete_name][table_second_complete_name]["on"] = on_generation

    def get_all_tables(self) -> dict:
        return self.__short_tables_dictionary

    def get_joins_dictionary(self) -> dict:
        """Returns joins with dictionary"""
        return self.__joins_dict

    def get_joins_by_table_dictionary(self) -> dict:
        """Returns dictionary with tables and their properties"""
        return self.__joins_by_table

    def get_filters_dictionary(self) -> dict:
        """Returns dictionary with filters"""
        return self.__filters_dict

    def get_all_fields(self) -> dict:
        """Returns dictionary with all fields"""
        return self.__complete_dict_of_fields


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
    print(c.get_joins_dictionary())
