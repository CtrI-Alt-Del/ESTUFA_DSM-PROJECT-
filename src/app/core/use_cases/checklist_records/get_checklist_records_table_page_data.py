from math import ceil

from core.entities import Plant, CheckListRecord
from core.constants import PAGINATION_LIMIT

from infra.repositories import plants_repository, checklist_records_repository


class GetChecklistRecordsTablePageData:
    def execute(
        self, page_number: int = 1, should_get_plants: bool = False
    ) -> tuple[list[CheckListRecord], int, list[Plant]]:
        plants = []
        if should_get_plants:
            plants = plants_repository.get_plants()

        checklist_records = checklist_records_repository.get_filtered_checklist_records(
            page_number=int(page_number)
        )

        checklist_count = checklist_records_repository.get_checklist_records_count()

        pages_count = ceil(checklist_count / PAGINATION_LIMIT)

        return checklist_records, pages_count, plants
