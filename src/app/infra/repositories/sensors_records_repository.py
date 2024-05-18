from core.entities import SensorsRecord, Datetime, Plant
from core.constants import PAGINATION

from infra.database import mysql

from datetime import date


class SensorRecordsRepository:
    def create_sensors_record(self, sensors_record: SensorsRecord) -> None:
        sql = """
        INSERT INTO sensors_records (soil_humidity, ambient_humidity, temperature, water_volume, created_at, plant_id) 
        VALUES (%s, %s, %s, %s, %s , %s)
        """

        mysql.mutate(
            sql=sql,
            params=[
                sensors_record.soil_humidity,
                sensors_record.ambient_humidity,
                sensors_record.temperature,
                sensors_record.water_volume,
                sensors_record.created_at.get_value(),
                sensors_record.plant.id,
            ],
        )

    def get_sensor_records_grouped_by_date(self):
        sql = """
        SELECT 
            DATE(created_at) AS date, 
            ROUND(AVG(soil_humidity), 1) AS soil_humidity,
            ROUND(AVG(ambient_humidity), 1) AS ambient_humidity,
            ROUND(AVG(temperature), 1) AS temperature,
            ROUND(AVG(water_volume), 1) AS water_volume,
            plant_id
        FROM sensors_records
        GROUP BY date, plant_id
        ORDER BY date ASC
        LIMIT 500;
        """
        rows = mysql.query(sql=sql, is_single=False)

        return rows

    def get_last_sensors_records(self, count) -> list[SensorsRecord]:
        rows = mysql.query(
            sql=f"""
            SELECT 
                SR.*, 
                P.id AS plant_id, 
                P.name AS plant_name,
                P.hex_color AS plant_color
            FROM sensors_records AS SR
            JOIN plants AS P ON P.id = SR.plant_id
            ORDER BY created_at DESC
            LIMIT {count};
            """,
            is_single=False,
        )

        if len(rows) == 0:
            return []

        return [self.__get_sensors_record_entity(row) for row in rows]

    

    def get_sensors_record_by_id(self, id: str) -> SensorsRecord | None:
        row = mysql.query(
            sql="""
            SELECT SR.*, P.id AS plant_id, P.name AS plant_name, P.hex_color AS plant_color
            FROM sensors_records AS SR 
            JOIN plants AS P ON P.id = SR.plant_id
            WHERE SR.id = %s
            """,
            is_single=True,
            params=[id],
        )

        if row:
            return self.__get_sensors_record_entity(row)

        return None

    def get_sensors_records_count(self) -> int:
        result = mysql.query(
            sql="SELECT COUNT(*) AS count FROM sensors_records",
            is_single=True,
        )

        return result["count"]

    def update_sensors_record_by_id(self, sensors_record: SensorsRecord) -> None:
        mysql.mutate(
            """
            UPDATE sensors_records
            SET
                soil_humidity = %s,
                ambient_humidity = %s,
                temperature = %s,
                water_volume = %s,
                created_at = %s,
                plant_id = %s
            WHERE id = %s
            """,
            params=[
                sensors_record.soil_humidity,
                sensors_record.ambient_humidity,
                sensors_record.temperature,
                sensors_record.water_volume,
                sensors_record.created_at.get_value(),
                sensors_record.plant.id,
                sensors_record.id,
            ],
        )

    def delete_sensors_record_by_id(self, sensors_record_id: str):
        mysql.mutate(
            "DELETE FROM sensors_records WHERE id = %s",
            params=[sensors_record_id],
        )

    def __get_sensors_record_entity(self, row: dict) -> SensorsRecord:
        if row:
            created_at = Datetime(row["created_at"])
            plant = Plant(
                id=row["plant_id"], name=row["plant_name"], hex_color=row["plant_color"]
            )

            return SensorsRecord(
                id=row["id"],
                ambient_humidity=int(row["ambient_humidity"]),
                soil_humidity=int(row["soil_humidity"]),
                temperature=float(row["temperature"]),
                water_volume=float(row["water_volume"]),
                plant=plant,
                created_at=created_at,
            )
        else:
            return None
    
    def get_filtered_sensors_records(self, plant_id: str,start_date: date,end_date: date,page_number: int = 1) -> list[SensorsRecord]:
        filters = []
        
        if plant_id:
            filters.append(f"SR.plant_id = '{plant_id}'")
            
        if start_date and end_date:
            filters.append(f"SR.created_at BETWEEN '{start_date} 00:)00:00' AND '{end_date} 23:59:59'")
        
        where = ""
        if len(filters) > 0:
            where = "WHERE" + "AND".join(filters)
        pagination_limit = PAGINATION["records_per_page"]
        offset = (page_number - 1) * pagination_limit
        
        rows = mysql.query(
            sql = f"""
            SELECT
                SR.*,
                P.id as plant_id,
                P.name AS plant_name,
                P.hex_color as plant_color
            FROM sensors_records AS SR
            JOIN plants AS P on P.id = SR.plant_id
            {where}
            ORDER BY SR.created_at DESC
            LIMIT {pagination_limit} OFFSET {offset}
            """,
            is_single=False
        )
        sensors_records = []
        
        if len(rows) > 0:
            for row in rows:
                sensors_records.append(self.__get_sensors_record_entity(row))
        return sensors_records
