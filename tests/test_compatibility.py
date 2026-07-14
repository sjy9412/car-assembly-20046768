from models.car import Car
from models.parts import Brake, CarType, Engine, Steering
from services.compatibility import check_compatibility


class TestCompatibilityRules:
    # 규칙 1: Continental 제동장치 → Sedan 불가
    def test_continental_sedan_fail(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        assert check_compatibility(car).is_compatible is False

    def test_continental_suv_pass(self):
        car = Car(car_type=CarType.SUV, engine=Engine.GM, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        assert check_compatibility(car).is_compatible is True

    def test_continental_truck_pass(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.GM, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        assert check_compatibility(car).is_compatible is True

    # 규칙 2: TOYOTA 엔진 → SUV 불가
    def test_toyota_suv_fail(self):
        car = Car(car_type=CarType.SUV, engine=Engine.TOYOTA, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is False

    def test_toyota_sedan_pass(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.TOYOTA, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is True

    def test_toyota_truck_pass(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.TOYOTA, brake=Brake.BOSCH_B, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is True

    # 규칙 3: WIA 엔진 → Truck 불가
    def test_wia_truck_fail(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.WIA, brake=Brake.BOSCH_B, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is False

    def test_wia_sedan_pass(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.WIA, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is True

    def test_wia_suv_pass(self):
        car = Car(car_type=CarType.SUV, engine=Engine.WIA, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        assert check_compatibility(car).is_compatible is True

    # 규칙 4: MANDO 제동장치 → Truck 불가
    def test_mando_truck_fail(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is False

    def test_mando_sedan_pass(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is True

    def test_mando_suv_pass(self):
        car = Car(car_type=CarType.SUV, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is True

    # 규칙 5: Bosch 제동장치 → Bosch 조향장치 필수
    def test_bosch_brake_non_bosch_steering_fail(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.BOSCH_B, steering=Steering.MOBIS)
        assert check_compatibility(car).is_compatible is False

    def test_bosch_brake_bosch_steering_pass(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.BOSCH_B, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is True

    # 결과 메시지 검증
    def test_fail_result_contains_fail_prefix(self):
        car = Car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.CONTINENTAL, steering=Steering.MOBIS)
        result = check_compatibility(car)
        assert result.message is not None
        assert result.message.startswith("FAIL")

    def test_pass_result_has_no_message(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.GM, brake=Brake.BOSCH_B, steering=Steering.BOSCH_S)
        result = check_compatibility(car)
        assert result.is_compatible is True
        assert result.message is None

    # 모든 규칙 통과하는 정상 조합
    def test_fully_valid_combination(self):
        car = Car(car_type=CarType.TRUCK, engine=Engine.GM, brake=Brake.BOSCH_B, steering=Steering.BOSCH_S)
        assert check_compatibility(car).is_compatible is True
