from flask import Flask

from query_builder.universe.structure_generator import StructureGenerator


class ComradeWolfFlask(Flask):
    # Stores StructureGenerator app-wide
    __structure_generator: StructureGenerator | None = None

    def set_structure_generator(self, structure_generator: StructureGenerator):
        """
        Updates the structure generator
        :param structure_generator: Structure generator
        :return:
        """
        self.__structure_generator = structure_generator

    def get_structure_generator(self) -> StructureGenerator:
        return self.__structure_generator
