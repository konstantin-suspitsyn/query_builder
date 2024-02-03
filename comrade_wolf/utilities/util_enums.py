import enum


class FlashType(enum.Enum):
    """
    To set class like in https://getbootstrap.com/docs/5.0/components/alerts/
    """
    info = "primary"
    warning = "danger"
    success = "success"
