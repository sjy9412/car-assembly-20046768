from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional

from models.car import Car
from models.parts import Brake, CarType, Engine, Steering


@dataclass
class CompatibilityRule:
    description: str
    condition: Callable[[Car], bool]  # True이면 규칙 위반


@dataclass
class CompatibilityResult:
    is_compatible: bool
    message: Optional[str] = None


RULES: list[CompatibilityRule] = [
    CompatibilityRule(
        description="Sedan에는 Continental제동장치 사용 불가",
        condition=lambda car: car.car_type == CarType.SEDAN and car.brake == Brake.CONTINENTAL,
    ),
    CompatibilityRule(
        description="SUV에는 TOYOTA엔진 사용 불가",
        condition=lambda car: car.car_type == CarType.SUV and car.engine == Engine.TOYOTA,
    ),
    CompatibilityRule(
        description="Truck에는 WIA엔진 사용 불가",
        condition=lambda car: car.car_type == CarType.TRUCK and car.engine == Engine.WIA,
    ),
    CompatibilityRule(
        description="Truck에는 Mando제동장치 사용 불가",
        condition=lambda car: car.car_type == CarType.TRUCK and car.brake == Brake.MANDO,
    ),
    CompatibilityRule(
        description="Bosch제동장치에는 Bosch조향장치 이외 사용 불가",
        condition=lambda car: car.brake == Brake.BOSCH_B and car.steering != Steering.BOSCH_S,
    ),
]


def check_compatibility(car: Car) -> CompatibilityResult:
    for rule in RULES:
        if rule.condition(car):
            return CompatibilityResult(is_compatible=False, message=f"FAIL\n{rule.description}")
    return CompatibilityResult(is_compatible=True)
