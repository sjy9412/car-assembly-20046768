from models.car import Car
from models.parts import Brake, CarType, Engine, Steering
from services.assembler import Assembler


class TestAssemblerValidate:
    def setup_method(self):
        self.assembler = Assembler()

    def test_valid_combination_is_compatible(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert self.assembler.validate(car).is_compatible is True

    def test_incompatible_combination_is_not_compatible(self):
        car = Car(car_type=CarType.SUV, engine=Engine.TOYOTA, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert self.assembler.validate(car).is_compatible is False

    def test_validate_returns_compatibility_result_with_message_on_fail(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        result = self.assembler.validate(car)
        assert result.is_compatible is False
        assert result.message is not None


class TestAssemblerCanRun:
    def setup_method(self):
        self.assembler = Assembler()

    def test_valid_combination_can_run(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert self.assembler.can_run(car) is True

    def test_truck_gm_bosch_bosch_can_run(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.GM, brake=Brake.BOSCH_B, steering=Steering.BOSCH_S)
        assert self.assembler.can_run(car) is True

    def test_broken_engine_cannot_run(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.BROKEN, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert self.assembler.can_run(car) is False

    def test_incompatible_combination_cannot_run(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        assert self.assembler.can_run(car) is False

    def test_broken_engine_with_valid_parts_cannot_run(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.BROKEN, brake=Brake.BOSCH_B, steering=Steering.BOSCH_S)
        assert self.assembler.can_run(car) is False

    def test_incompatible_and_broken_engine_cannot_run(self):
        car = Car(car_type=CarType.SUV, engine=Engine.BROKEN, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        assert self.assembler.can_run(car) is False
