from query_builder.universe.structure_generator import StructureGenerator


def create_structure_generator(app, joins_path: str, tables_path: str, standard_fields_path: str):
    """
    Generates Structure Generator
    :param app:
    :param joins_path:
    :param tables_path:
    :param standard_fields_path:
    :return:
    """

    app.structure_generator = StructureGenerator(tables_path, joins_path, standard_fields_path)
