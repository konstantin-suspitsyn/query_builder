from query_builder.universe.structure_generator import StructureGenerator


def create_structure_generator(joins_path: str, tables_path: str, standard_fields_path: str) -> StructureGenerator:
    """
    Generates Structure Generator
    :param joins_path:
    :param tables_path:
    :param standard_fields_path:
    :return:
    """

    return StructureGenerator(tables_path, joins_path, standard_fields_path)
