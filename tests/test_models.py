from models.parts import CarType, Engine, Brake, Steering
from models.car import Car


class TestCarIsComplete:
    def test_empty_car_is_not_complete(self):
        assert Car().is_complete() is False

    def test_only_car_type_is_not_complete(self):
        assert Car(car_type=CarType.SEDAN).is_complete() is False

    def test_three_parts_is_not_complete(self):
        car = Car(car_type=CarType.SUV, engine=Engine.GM, brake=Brake.MANDO)
        assert car.is_complete() is False

    def test_all_four_parts_is_complete(self):
        car = Car(
            car_type=CarType.SEDAN,
            engine=Engine.GM,
            brake=Brake.MANDO,
            steering=Steering.BOSCH_S,
        )
        assert car.is_complete() is True

    def test_broken_engine_counts_as_complete(self):
        car = Car(
            car_type=CarType.TRUCK,
            engine=Engine.BROKEN,
            brake=Brake.BOSCH_B,
            steering=Steering.BOSCH_S,
        )
        assert car.is_complete() is True


class TestCarReset:
    def test_reset_clears_all_fields(self):
        car = Car(
            car_type=CarType.SUV,
            engine=Engine.TOYOTA,
            brake=Brake.CONTINENTAL,
            steering=Steering.MOBIS,
        )
        car.reset()
        assert car.car_type is None
        assert car.engine is None
        assert car.brake is None
        assert car.steering is None

    def test_reset_makes_car_incomplete(self):
        car = Car(
            car_type=CarType.SEDAN,
            engine=Engine.GM,
            brake=Brake.MANDO,
            steering=Steering.BOSCH_S,
        )
        car.reset()
        assert car.is_complete() is False

    def test_reset_on_empty_car_is_idempotent(self):
        car = Car()
        car.reset()
        assert car.is_complete() is False
