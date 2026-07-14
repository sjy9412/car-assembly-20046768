from models.car import Car
from models.parts import Engine
from services.compatibility import CompatibilityResult, check_compatibility


class Assembler:
    def validate(self, car: Car) -> CompatibilityResult:
        return check_compatibility(car)

    def can_run(self, car: Car) -> bool:
        if not self.validate(car).is_compatible:
            return False
        if car.engine == Engine.BROKEN:
            return False
        return True
