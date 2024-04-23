from dataclasses import dataclass

from core.entities.entity import Entity

@dataclass
class PlantsRecord(Entity):
    name: str = None
    hex_color: str = None