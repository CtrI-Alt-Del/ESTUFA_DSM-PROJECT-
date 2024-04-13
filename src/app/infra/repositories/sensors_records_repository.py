from typing import List, Dict

from core.entities.sensors_record import SensorsRecord

from infra.database import mysql


class SensorRecordsRepository:
    def create_sensors_record(self, sensors_record: SensorsRecord) -> None:
        sql = """
        INSERT INTO sensors_records (soil_humidity, ambient_humidity, temperature, water_volume, created_at) 
        VALUES (%s, %s, %s, %s, %s)
        """
        mysql.mutate(
            sql=sql,
            params=[
                sensors_record.soil_humidity,
                sensors_record.ambient_humidity,
                sensors_record.temperature,
                sensors_record.water_volume,
                sensors_record.created_at,
            ],
        )

    def get_sensor_records_grouped_by_date(self) -> List[SensorsRecord]:
        sql = """
        SELECT 
            DATE(created_at) AS date, 
            ROUND(AVG(soil_humidity), 1) AS soil_humidity,
            ROUND(AVG(ambient_humidity), 1) AS ambient_humidity,
            ROUND(AVG(temperature), 1) AS temperature,
            ROUND(AVG(water_volume), 1) AS water_volume
        FROM sensors_records
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at) ASC
        LIMIT 500;
        """
        rows = mysql.query(sql=sql, is_single=False)

        return rows

    def _get_sensors_record(self, row: Dict) -> SensorsRecord:
        if row:
            return SensorsRecord(
                ambient_humidity=row["ambient_humidity"],
                soil_humidity=row["soil_humidity"],
                temperature=row["temperature"],
                water_volume=row["water_volume"],
                created_at=row["created_at"],
            )
        else:
            return None
