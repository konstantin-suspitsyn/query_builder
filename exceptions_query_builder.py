class UnknownTableTypeProperty(Exception):
    """
    Exception if an extra table_type appeared
    """

    def __init__(self, table_name: str, table_type: str) -> None:
        message = f"В таблице {table_name} проставлен тип таблицы {table_type}, что не соответствует закрытому списку"
        super().__init__(message)


class UnknownTableFieldProperty(Exception):
    """
    Exception if an extra table_type appeared
    """

    def __init__(self, table_name: str, field_name: str, field_type: str) -> None:
        message = f"В таблице {table_name} у поля {field_name} проставлен неизвестный тип поля {field_type}"
        super().__init__(message)


class UnknownTableType(Exception):
    def __init__(self, table_name: str, table_type: str) -> None:
        message = f"Неизвестный тип таблицы {table_name}: {table_type}"
        super().__init__(message)
