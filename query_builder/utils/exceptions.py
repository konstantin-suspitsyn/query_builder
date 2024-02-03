class RepeatingTableException(Exception):
    """
    Error is thrown where we got two or more objects with repeating names
    """

    def __init__(self, file_name: str, name: str, duplicate_key_name: str) -> None:
        message = f"В файле {file_name} обнаружен дубликат {duplicate_key_name} {name}"
        super().__init__(message)


class NoMandatoryKeyException(Exception):
    """
    Exception if imported data doesn't have mandatory key
    """

    def __init__(self, file_name: str, key: str) -> None:
        message = f"В файле {file_name} не найден ключ {key}"
        super().__init__(message)


class UnknownTypeOfImport(Exception):
    """
    Exception if type of import not one of ImportTypes.values
    """

    def __init__(self, type_of_import: str) -> None:
        message = f"Неизвестный тип импорта {type_of_import}"
        super().__init__(message)


class NoHumanNameForShownField(Exception):
    """
    Error when setting field to show and not giving it a name
    """

    def __init__(self, field_name: str) -> None:
        message = f"Показатель show поля {field_name} == True, при этом поле \"name\" не представлено"
        super().__init__(message)


class UnknownFieldTypeForField(Exception):
    """
    Exception if type of field not in FieldType
    """

    def __init__(self, field_name: str, field_type: str) -> None:
        message = f"Неизвестный тип поля {field_type} для {field_name}"
        super().__init__(message)


class UnknownFieldType(Exception):
    """
    Exception if type of field not in FieldType
    """

    def __init__(self, field_type: str) -> None:
        message = f"Неизвестный тип поля {field_type}"
        super().__init__(message)


class FieldsFromFrontendWrongValue(Exception):
    """
    Exception if any value under key of FieldsFromFrontend class is not list
    """

    def __init__(self, key: str) -> None:
        message = f"Все поступающие значения внутри словаря должны быть типом list. Проверь {key}"
        super().__init__(message)


class UnknownTableType(Exception):
    def __init__(self, table_name: str, table_type: str) -> None:
        message = f"Неизвестный тип таблицы {table_name}: {table_type}"
        super().__init__(message)
