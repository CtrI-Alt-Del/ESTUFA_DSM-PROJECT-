from flask import render_template

from core.commons import Error

from infra.forms import SensorsRecordForm
from infra.repositories import sensors_records_repository


def update_sensors_record_form_view(id: str):
    try:
        sensors_record = sensors_records_repository.get_sensors_record_by_id(id)

        update_sensors_record_form = SensorsRecordForm(sensors_record=sensors_record)

        return render_template(
            "pages/sensors_records_table/update_sensors_record_form/index.html",
            sensors_record_id=sensors_record.id,
            update_sensors_record_form=update_sensors_record_form,
        )
    except Error as error:
        return "Registro não encontrado 😢", error.status_code
