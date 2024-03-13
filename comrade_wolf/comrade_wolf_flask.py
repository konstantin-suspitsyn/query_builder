from flask import Flask

from query_builder.universe.frontend_backend_converter import FrontendBackendConverter
from query_builder.universe.joins_generator import GenerateJoins
from query_builder.universe.possible_joins import AllPossibleJoins
from query_builder.universe.query_generator import QueryGenerator
from query_builder.universe.structure_generator import StructureGenerator
from query_builder.utils.data_types import FieldsForQuery
from query_builder.utils.language_specific_builders import PostgresCalculationBuilder, BaseCalculationBuilder


class ComradeWolfFlask(Flask):
    # Stores StructureGenerator app-wide
    __structure_generator: StructureGenerator | None = None
    __frontend_backend_converter: FrontendBackendConverter | None = None
    __query_generator: QueryGenerator | None = None
    __calculation_builder: BaseCalculationBuilder | None = None

    def set_structure_generator(self, structure_generator: StructureGenerator):
        """
        Updates the structure generator
        :param structure_generator: Structure generator
        :return:
        """
        self.__structure_generator = structure_generator
        self.__calculation_builder = PostgresCalculationBuilder()

        self.__query_generator = QueryGenerator(self.__structure_generator.get_tables(),
                                                self.__structure_generator.get_fields(),
                                                self.__structure_generator.get_where(),
                                                self.__calculation_builder)

        GenerateJoins(self.__structure_generator.get_joins(), self.__structure_generator.get_tables())
        AllPossibleJoins()

        self.__frontend_backend_converter = FrontendBackendConverter(self.__structure_generator.get_fields(),
                                                                     self.__structure_generator.get_tables(),
                                                                     self.__structure_generator.get_where(),
                                                                     self.__calculation_builder)

    def get_structure_generator(self) -> StructureGenerator:
        return self.__structure_generator

    def get_frontend_backend_converter(self) -> FrontendBackendConverter:
        return self.__frontend_backend_converter

    def build_query(self, frontend_fields: dict) -> str:
        front_to_back: FieldsForQuery = self.__frontend_backend_converter.convert_from_frontend_to_backend(
            frontend_fields)

        query: str = self.__query_generator.generate_query(front_to_back)

        return query
