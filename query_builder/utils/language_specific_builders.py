class BaseCalculationBuilder:
    """
    Base class for all basic calculation builders
    """

    def generate_calculation(self, field_name: str, calculation_type: str):
        if calculation_type == "sum":
            return self.generate_sum(field_name)

        if calculation_type == "avg":
            return self.generate_avg(field_name)

        if calculation_type == "min":
            return self.generate_min(field_name)

        if calculation_type == "max":
            return self.generate_max(field_name)

        if calculation_type == "count":
            return self.generate_count(field_name)

        if calculation_type == "count distinct":
            return self.generate_count_distinct(field_name)

    def generate_sum(self, field_name: str) -> str:
        pass

    def generate_avg(self, field_name: str) -> str:
        pass

    def generate_count_distinct(self, field_name: str) -> str:
        pass

    def generate_max(self, field_name: str) -> str:
        pass

    def generate_min(self, field_name: str) -> str:
        pass

    def generate_count(self, field_name: str) -> str:
        pass


class PostgresCalculationBuilder(BaseCalculationBuilder):
    def generate_sum(self, field_name: str) -> str:
        return "SUM({})".format(field_name)

    def generate_avg(self, field_name: str) -> str:
        return "AVG({})".format(field_name)

    def generate_count_distinct(self, field_name: str) -> str:
        return "COUNT(DISTINCT {})".format(field_name)

    def generate_max(self, field_name: str) -> str:
        return "MAX({})".format(field_name)

    def generate_min(self, field_name: str) -> str:
        return "MIN({})".format(field_name)

    def generate_count(self, field_name: str) -> str:
        return "COUNT({})".format(field_name)
