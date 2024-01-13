import os
import warnings

import toml

from query_builder.utils.data_types import TableTomlImport, JoinsTomlImport
from query_builder.utils.enums_and_field_dicts import ImportTypes
from query_builder.utils.exceptions import RepeatingTableException, UnknownTypeOfImport


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


def gather_data_from_toml_files_into_big_dictionary(list_of_files: list,
                                                    check_for_duplicate_key: str) -> dict:
    """
    Gathers data from toml files and check for duplicates and mandatory fields
    :param list_of_files: list with paths to toml files and one of ImportTypes.values
    :param check_for_duplicate_key: name of key to check for duplicates. So we would not have two same tables
    :return: dictionary from all files
    """

    # Check if outer_type exists in type field
    all_types = [f.value for f in ImportTypes]

    if check_for_duplicate_key not in all_types:
        raise UnknownTypeOfImport(check_for_duplicate_key)

    result: dict = {}

    for file in list_of_files:
        temp_toml: dict = toml.load(file)

        non_duplicate_key = temp_toml[check_for_duplicate_key]

        if non_duplicate_key in result:
            raise RepeatingTableException(file, non_duplicate_key, check_for_duplicate_key)

        if check_for_duplicate_key == ImportTypes.TABLE.value:
            result[non_duplicate_key] = TableTomlImport(temp_toml, file)

        if check_for_duplicate_key == ImportTypes.JOINS.value:
            result[non_duplicate_key] = JoinsTomlImport(temp_toml, file)

        if check_for_duplicate_key == ImportTypes.FILTERS.value:
            result[non_duplicate_key] = temp_toml

    return result
