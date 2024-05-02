from dataclasses import dataclass

from core.entities.entity import Entity
from core.commons.datetime import Datetime
from core.entities.plant import Plant


@dataclass
class SensorsRecord(Entity):
    soil_humidity: int = None
    ambient_humidity: int = None
    water_volume: float = None
    temperature: float = None
    created_at: Datetime = None
    plant: Plant = None
