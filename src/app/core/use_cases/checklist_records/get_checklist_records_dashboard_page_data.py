from core.constants import LEAF_APPEARANCES, LEAF_COLORS
from core.commons import Error, LineChart

from infra.repositories import checklist_records_repository, plants_repository


class GetChecklistRecordsDashboardPageData:
    def execute(self):
        try:
            plants = plants_repository.get_plants()

            if len(plants) == 0:
                raise Error("Nenhuma planta encontrada", status_code=404)

            leaf_records = (
                checklist_records_repository.get_leaf_appearances_and_leaf_colors_records()
            )

            if len(leaf_records) == 0:
                raise Error("Nenhum registro de check-list encontrado", status_code=404)

            leaf_charts_data = self.__get_leaf_charts_data(leaf_records, plants)

            lai_records = checklist_records_repository.get_lai_records()

            if len(lai_records) == 0:
                raise Error("Nenhum registro de check-list encontrado", status_code=404)

            plant_growth_chart = LineChart(lai_records, "lai")

            return {
                **leaf_charts_data,
                "plant_growth_chart_data": plant_growth_chart.get_data(plants),
                "plants": plants,
            }
        except Error as error:
            raise error

    def __get_leaf_charts_data(self, records, plants):
        days_count_by_leaf_appearance_and_plant = {
            plant.id: {leaf_appearance: 0 for leaf_appearance in LEAF_APPEARANCES}
            for plant in plants
        }

        days_count_by_leaf_color_and_plant = {
            plant.id: {leaf_color: 0 for leaf_color in LEAF_COLORS} for plant in plants
        }

        for plant in plants:
            for leaf_appearance in LEAF_APPEARANCES:
                for record in records:
                    if (
                        record["leaf_appearance"] == leaf_appearance
                        and record["plant_id"] == plant.id
                    ):
                        print(days_count_by_leaf_appearance_and_plant, flush=True)
                        days_count_by_leaf_appearance_and_plant[plant.id][
                            leaf_appearance
                        ] += 1

            for leaf_color in LEAF_COLORS:
                for record in records:
                    if (
                        record["leaf_color"] == leaf_color
                        and record["plant_id"] == plant.id
                    ):
                        days_count_by_leaf_color_and_plant[plant.id][leaf_color] += 1

        print(days_count_by_leaf_appearance_and_plant, flush=True)
        return {
            "days_count_by_leaf_appearance_and_plant": days_count_by_leaf_appearance_and_plant,
            "days_count_by_leaf_color_and_plant": days_count_by_leaf_color_and_plant,
        }
