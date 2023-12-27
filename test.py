from enum_query_builder import TomlTableTableTypeFieldPossibleValues


def test():
    for word in TomlTableTableTypeFieldPossibleValues:
        print(word.value)


if __name__ == "__main__":
    test()
