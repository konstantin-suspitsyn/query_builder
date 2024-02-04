from flask import Flask

from query_builder.universe.structure_generator import StructureGenerator


class ComradeWolfFlask(Flask):
    # Stores StructureGenerator app-wide
    structure_generator: StructureGenerator | None = None

    def update_structure_generator(self, structure_generator: StructureGenerator):
        """
        Updates the structure generator
        :param structure_generator: Structure generator
        :return:
        """
        self.structure_generator = structure_generator
