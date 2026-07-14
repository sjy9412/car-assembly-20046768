from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from models.parts import CarType, Engine, Brake, Steering


@dataclass
class Car:
    car_type: Optional[CarType] = None
    engine: Optional[Engine] = None
    brake: Optional[Brake] = None
    steering: Optional[Steering] = None

    def is_complete(self) -> bool:
        return all(
            part is not None
            for part in (self.car_type, self.engine, self.brake, self.steering)
        )

    def reset(self) -> None:
        self.car_type = None
        self.engine = None
        self.brake = None
        self.steering = None
