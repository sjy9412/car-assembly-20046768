import sys
import time

from models.car import Car
from models.parts import Brake, CarType, Engine, Steering
from services.assembler import Assembler
from services.compatibility import check_compatibility

CLEAR_SCREEN = "\033[H\033[2J"

CarType_Q = 0
Engine_Q = 1
brakeSystem_Q = 2
SteeringSystem_Q = 3
Run_Test = 4

q0 = 0
q1 = 0
q2 = 0
q3 = 0


def delay(ms: int) -> None:
    time.sleep(ms / 1000.0)


def clear() -> None:
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def show_menu(step: int) -> None:
    clear()
    if step == 0:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
        print("1. Sedan")
        print("2. SUV")
        print("3. Truck")
    elif step == 1:
        print("어떤 엔진을 탑재할까요?")
        print("0. 뒤로가기")
        print("1. GM")
        print("2. TOYOTA")
        print("3. WIA")
        print("4. 고장난 엔진")
    elif step == 2:
        print("어떤 제동장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. MANDO")
        print("2. CONTINENTAL")
        print("3. BOSCH")
    elif step == 3:
        print("어떤 조향장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. BOSCH")
        print("2. MOBIS")
    elif step == 4:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")
    print("===============================")


def is_valid_range(step: int, ans: int) -> bool:
    if step == 0:
        if ans < 1 or ans > 3:
            print("ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능")
            return False
    if step == 1:
        if ans < 0 or ans > 4:
            print("ERROR :: 엔진은 0 ~ 4 범위만 선택 가능")
            return False
    if step == 2:
        if ans < 0 or ans > 3:
            print("ERROR :: 제동장치는 0 ~ 3 범위만 선택 가능")
            return False
    if step == 3:
        if ans < 0 or ans > 2:
            print("ERROR :: 조향장치는 0 ~ 2 범위만 선택 가능")
            return False
    if step == 4:
        if ans < 0 or ans > 2:
            print("ERROR :: Run 또는 Test 중 하나를 선택 필요")
            return False
    return True


def select_car_type(a: int) -> None:
    global q0
    q0 = a
    if a == 1:
        print("차량 타입으로 Sedan을 선택하셨습니다.")
    elif a == 2:
        print("차량 타입으로 SUV을 선택하셨습니다.")
    elif a == 3:
        print("차량 타입으로 Truck을 선택하셨습니다.")


def select_engine(a: int) -> None:
    global q1
    q1 = a
    if a == 1:
        print("GM 엔진을 선택하셨습니다.")
    elif a == 2:
        print("TOYOTA 엔진을 선택하셨습니다.")
    elif a == 3:
        print("WIA 엔진을 선택하셨습니다.")
    elif a == 4:
        print("고장난 엔진을 선택하셨습니다.")


def select_brake(a: int) -> None:
    global q2
    q2 = a
    if a == 1:
        print("MANDO 제동장치를 선택하셨습니다.")
    elif a == 2:
        print("CONTINENTAL 제동장치를 선택하셨습니다.")
    elif a == 3:
        print("BOSCH 제동장치를 선택하셨습니다.")


def select_steering(a: int) -> None:
    global q3
    q3 = a
    if a == 1:
        print("BOSCH 조향장치를 선택하셨습니다.")
    elif a == 2:
        print("MOBIS 조향장치를 선택하셨습니다.")


def _build_car() -> Car:
    return Car(
        car_type=CarType(q0) if q0 != 0 else None,
        engine=Engine(q1) if q1 != 0 else None,
        brake=Brake(q2) if q2 != 0 else None,
        steering=Steering(q3) if q3 != 0 else None,
    )


def show_run_result() -> None:
    car = _build_car()
    assembler = Assembler()
    if not assembler.validate(car).is_compatible:
        print("자동차가 동작되지 않습니다")
        return
    if not assembler.can_run(car):
        print("엔진이 고장나있습니다.")
        print("자동차가 움직이지 않습니다.")
        return

    car_type_labels = {
        CarType.SEDAN: "Sedan",
        CarType.SUV: "SUV",
        CarType.TRUCK: "Truck",
    }
    engine_labels = {
        Engine.GM: "GM",
        Engine.TOYOTA: "TOYOTA",
        Engine.WIA: "WIA",
    }
    brake_labels = {
        Brake.MANDO: "Mando",
        Brake.CONTINENTAL: "Continental",
        Brake.BOSCH_B: "Bosch",
    }
    steering_labels = {
        Steering.BOSCH_S: "Bosch",
        Steering.MOBIS: "Mobis",
    }

    print(f"Car Type : {car_type_labels.get(car.car_type, '')}")
    print(f"Engine   : {engine_labels.get(car.engine, '')}")
    print(f"Brake    : {brake_labels.get(car.brake, '')}")
    print(f"Steering : {steering_labels.get(car.steering, '')}")
    print("자동차가 동작됩니다.")


def show_test_result() -> None:
    result = check_compatibility(_build_car())
    if result.is_compatible:
        print("PASS")
    else:
        print(result.message)


def run() -> None:
    global q0, q1, q2, q3
    step = 0
    while True:
        show_menu(step)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not is_valid_range(step, ans):
            delay(800)
            continue

        if ans == 0:
            if step == 4:
                step = 0
            elif step > 0:
                step -= 1
            continue

        if step == 0:
            select_car_type(ans)
            delay(800)
            step = 1
        elif step == 1:
            select_engine(ans)
            delay(800)
            step = 2
        elif step == 2:
            select_brake(ans)
            delay(800)
            step = 3
        elif step == 3:
            select_steering(ans)
            delay(800)
            step = 4
        elif step == 4:
            if ans == 1:
                show_run_result()
                delay(2000)
            elif ans == 2:
                print("Test...")
                delay(1500)
                show_test_result()
                delay(2000)
