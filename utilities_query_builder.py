import re


def split_to_fields(calculation: str, full_table_name: str) -> list:
    """
    Splits calculation formula into fields. Ignores fields from current table
    :param calculation: calculation formula
    :param full_table_name:
    :return:
    """
    needed_fields = []

    # Get all inside sum()/ avg() and so on
    string_inside_brackets: str = re.search(r"\((.*?)\)", calculation).group(0)

    for item in ["(", ")", "+", "-", "*", "//"]:
        string_inside_brackets = string_inside_brackets.replace(item, " ")

    string_inside_brackets = re.sub(" +", " ", string_inside_brackets)

    for field in string_inside_brackets.split(" "):
        if (field != "") and (field[:len(full_table_name)] != full_table_name):
            needed_fields.append(field)

    return needed_fields
