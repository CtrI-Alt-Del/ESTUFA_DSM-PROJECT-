from flask import render_template, request

from core.use_cases.sensors_records import update_sensors_records
from core.commons import Error

from infra.forms import SensorsRecordForm


def update_sensors_record_view(id: str):
    sensors_record_form = SensorsRecordForm(request.form)

    try:
        if not sensors_record_form.validate_on_submit():
            raise Error("Formulário inválido")

        updated_sensors_record = update_sensors_records.execute(
            {
                "soil_humidity": sensors_record_form.soil_humidity.data,
                "ambient_humidity": sensors_record_form.ambient_humidity.data,
                "temperature": sensors_record_form.temperature.data,
                "water_volume": sensors_record_form.water_volume.data,
                "plant_id": sensors_record_form.plant_id.data,
                "time": sensors_record_form.time.data,
                "date": sensors_record_form.date.data,
                "sensors_record_id": id,
            },
        )

        return render_template(
            "pages/sensors_records_table/row.html",
            sensors_record=updated_sensors_record,
        )
    except Error as error:
        print(error.ui_message, flush=True)
        print(sensors_record_form.errors, flush=True)
        return "ERROR", error.status_code
