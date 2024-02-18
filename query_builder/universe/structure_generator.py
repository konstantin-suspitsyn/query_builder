from query_builder.utils.enums_and_field_dicts import ImportTypes, FieldType, FrontFieldTypes
from query_builder.utils.exceptions import NoHumanNameForShownField, UnknownFieldTypeForField, UnknownFrontFieldType
from query_builder.utils.utils import gather_data_from_toml_files_into_big_dictionary, list_toml_files_in_directory, \
    true_false_converter


class StructureGenerator:
    """
    Generates dictionary-like objects with table-structures and joins
    """

    # Dictionary with structure {"table_name": "table_type"}
    __short_tables_dictionary: dict = {}
    __joins_by_table: dict = {}
    # All fields with properties
    __all_fields: dict = {}

    # Table name structure database.scheme.table
    TABLE_NAME_STRUCTURE: str = "{}.{}.{}"
    # Table name structure database.scheme.table.field_name
    FIELD_NAME: str = "{}.{}.{}.{}"

    def __init__(self, tables_folder_link: str, joins_folder_link: str, filters_folder_link: str) -> None:
        """
        Gets data from all toml files
        Checks for duplicates and other errors
        :param tables_folder_link: link to folder with .toml files, containing table references
        :param filters_folder_link: link to folder with .toml files, containing filters references
        :param joins_folder_link: link to folder with .toml files, containing joins references
        """

        self.__short_tables_dictionary = {}
        self.__joins_by_table = {}
        self.__all_fields = {}

        toml_tables: dict = gather_data_from_toml_files_into_big_dictionary(
            list_toml_files_in_directory(tables_folder_link), ImportTypes.TABLE.value)
        toml_joins_dict: dict = gather_data_from_toml_files_into_big_dictionary(
            list_toml_files_in_directory(joins_folder_link), ImportTypes.JOINS.value)
        toml_filters_dict: dict = gather_data_from_toml_files_into_big_dictionary(
            list_toml_files_in_directory(filters_folder_link), ImportTypes.FILTERS.value)

        self.__generate_short_tables_dictionary(toml_tables)
        self.__create_all_fields(toml_tables)
        self.__create_all_joins(toml_joins_dict)

    def __generate_short_tables_dictionary(self, toml_tables: dict) -> None:
        """
        Generates __short_tables_dictionary
        :param toml_tables: dictionary created from toml files containing tables
        :return: None
        """
        for file_name in toml_tables:
            table_type = toml_tables[file_name]["table_type"]
            complete_table_name = self.TABLE_NAME_STRUCTURE.format(
                toml_tables[file_name]["database"],
                toml_tables[file_name]["schema"],
                toml_tables[file_name]["table"])
            self.__short_tables_dictionary[complete_table_name] = table_type

    def __create_all_fields(self, toml_tables: dict) -> None:
        """
        Creates self.__all_fields
        :param toml_tables: created in self.__init__
        :return:
        """

        field_types_check = [f.value for f in FieldType]
        front_field_list_check = [f.value for f in FrontFieldTypes]

        for file_name in toml_tables:

            # Working with usual fields
            for field in toml_tables[file_name]["fields"]:

                field_name = self.FIELD_NAME.format(
                    toml_tables[file_name]["database"],
                    toml_tables[file_name]["schema"],
                    toml_tables[file_name]["table"],
                    field)
                field_type: str = toml_tables[file_name]["fields"][field]["type"]

                if field_type not in field_types_check:
                    raise UnknownFieldTypeForField(field_name, field_type)

                field_show: bool = true_false_converter(toml_tables[file_name]["fields"][field]["show"])

                front_field_type: str | None = None

                if field_show:
                    # Check if front_field type exists and in enum
                    front_field_type = toml_tables[file_name]["fields"][field]["front_type"]
                    if front_field_type not in front_field_list_check:
                        raise UnknownFrontFieldType(field_name, front_field_type)

                show_group: str | None = None
                if "show_group" in toml_tables[file_name]["fields"][field]:
                    show_group = toml_tables[file_name]["fields"][field]["show_group"]

                # There is possibility than Human-name does not exist
                field_human_name: str | None = None

                # Check if name doesn't exist, show == False
                if ("name" not in toml_tables[file_name]["fields"][field]) and (field_show is True):
                    raise NoHumanNameForShownField(field_name)

                if "name" in toml_tables[file_name]["fields"][field]:
                    field_human_name = toml_tables[file_name]["fields"][field]["name"]

                self.__all_fields[field_name] = {
                    "name": field_human_name,
                    "show": field_show,
                    "type": field_type,
                    "show_group": show_group
                }

                if field_show:
                    self.__all_fields[field_name]["front_field_type"] = front_field_type

                # Working with predefined calculations
                if field_type == FieldType.CALCULATION.value:

                    field_calculation = toml_tables[file_name]["fields"][field]["calculation"]

                    field_where = None

                    if "where" in toml_tables[file_name]["fields"][field]:
                        field_where = toml_tables[file_name]["fields"][field]["where"]

                    self.__all_fields[field_name]["where"] = field_where
                    self.__all_fields[field_name]["calculation"] = field_calculation
                    self.__all_fields[field_name]["type"] = FieldType.CALCULATION.value

    def __create_all_joins(self, toml_joins_dict) -> None:
        """
        Creates all joins by every table and fills. Fills in self.__joins_by_table
        :param toml_joins_dict: created in self.__init__
        :return: None
        """
        for file_name in toml_joins_dict:

            if len(toml_joins_dict[file_name]["second_table"].keys()) == 0:
                continue

            table_name = self.TABLE_NAME_STRUCTURE.format(
                toml_joins_dict[file_name]["database"],
                toml_joins_dict[file_name]["schema"],
                toml_joins_dict[file_name]["first_table"],
            )

            if table_name not in self.__joins_by_table:
                self.__joins_by_table[table_name] = {}

            for join_table in toml_joins_dict[file_name]["second_table"]:
                self.__joins_by_table[table_name][join_table] = {}
                self.__joins_by_table[table_name][join_table]["how"] = toml_joins_dict[file_name]["second_table"][
                    join_table]["how"]
                self.__joins_by_table[table_name][join_table]["on"] = {}
                self.__joins_by_table[table_name][join_table]["on"]["between_tables"] = toml_joins_dict[file_name][
                    "second_table"][join_table]["between_tables"]
                self.__joins_by_table[table_name][join_table]["on"]["first_table_on"] = toml_joins_dict[file_name][
                    "second_table"][join_table]["first_table_on"]
                self.__joins_by_table[table_name][join_table]["on"]["second_table_on"] = toml_joins_dict[file_name][
                    "second_table"][join_table]["second_table_on"]

    def get_tables(self) -> dict:
        """
        Returns all tables
        :return: {"table_name": "table_type"}
        """
        return self.__short_tables_dictionary

    def get_fields(self) -> dict:
        """
        Returns all fields
        :return:
        """
        return self.__all_fields

    def get_joins(self) -> dict:
        """
        Returns all joins
        :return:
        """
        return self.__joins_by_table
