import runpy
from unittest.mock import patch

import pytest

import ui.menu as menu
from models.parts import Brake, CarType, Engine, Steering


@pytest.fixture(autouse=True)
def reset_globals():
    menu.q0 = 0
    menu.q1 = 0
    menu.q2 = 0
    menu.q3 = 0
    yield
    menu.q0 = 0
    menu.q1 = 0
    menu.q2 = 0
    menu.q3 = 0


class TestDelay:
    def test_converts_ms_to_seconds(self):
        with patch("ui.menu.time") as mock_time:
            menu.delay(500)
            mock_time.sleep.assert_called_once_with(0.5)

    def test_zero_ms(self):
        with patch("ui.menu.time") as mock_time:
            menu.delay(0)
            mock_time.sleep.assert_called_once_with(0.0)

    def test_one_second(self):
        with patch("ui.menu.time") as mock_time:
            menu.delay(1000)
            mock_time.sleep.assert_called_once_with(1.0)


class TestClear:
    def test_writes_escape_sequence_to_stdout(self, capsys):
        menu.clear()
        assert menu.CLEAR_SCREEN in capsys.readouterr().out


class TestShowMenu:
    def test_step0_shows_car_type_options(self, capsys):
        with patch("ui.menu.clear"):
            menu.show_menu(0)
        out = capsys.readouterr().out
        assert "차량 타입" in out
        assert "Sedan" in out
        assert "SUV" in out
        assert "Truck" in out

    def test_step1_shows_engine_options(self, capsys):
        with patch("ui.menu.clear"):
            menu.show_menu(1)
        out = capsys.readouterr().out
        assert "엔진" in out
        assert "GM" in out
        assert "TOYOTA" in out
        assert "WIA" in out
        assert "고장난 엔진" in out
        assert "뒤로가기" in out

    def test_step2_shows_brake_options(self, capsys):
        with patch("ui.menu.clear"):
            menu.show_menu(2)
        out = capsys.readouterr().out
        assert "제동장치" in out
        assert "MANDO" in out
        assert "CONTINENTAL" in out
        assert "BOSCH" in out

    def test_step3_shows_steering_options(self, capsys):
        with patch("ui.menu.clear"):
            menu.show_menu(3)
        out = capsys.readouterr().out
        assert "조향장치" in out
        assert "BOSCH" in out
        assert "MOBIS" in out

    def test_step4_shows_run_test_options(self, capsys):
        with patch("ui.menu.clear"):
            menu.show_menu(4)
        out = capsys.readouterr().out
        assert "완성" in out
        assert "RUN" in out
        assert "Test" in out
        assert "처음 화면으로 돌아가기" in out


class TestIsValidRange:
    def test_step0_valid_min(self):
        assert menu.is_valid_range(0, 1) is True

    def test_step0_valid_max(self):
        assert menu.is_valid_range(0, 3) is True

    def test_step0_invalid_zero(self, capsys):
        assert menu.is_valid_range(0, 0) is False
        assert "ERROR" in capsys.readouterr().out

    def test_step0_invalid_four(self, capsys):
        assert menu.is_valid_range(0, 4) is False

    def test_step1_valid_min(self):
        assert menu.is_valid_range(1, 0) is True

    def test_step1_valid_max(self):
        assert menu.is_valid_range(1, 4) is True

    def test_step1_invalid_negative(self, capsys):
        assert menu.is_valid_range(1, -1) is False
        assert "ERROR" in capsys.readouterr().out

    def test_step1_invalid_five(self, capsys):
        assert menu.is_valid_range(1, 5) is False

    def test_step2_valid_min(self):
        assert menu.is_valid_range(2, 0) is True

    def test_step2_valid_max(self):
        assert menu.is_valid_range(2, 3) is True

    def test_step2_invalid_negative(self, capsys):
        assert menu.is_valid_range(2, -1) is False
        assert "ERROR" in capsys.readouterr().out

    def test_step2_invalid_four(self, capsys):
        assert menu.is_valid_range(2, 4) is False

    def test_step3_valid_min(self):
        assert menu.is_valid_range(3, 0) is True

    def test_step3_valid_max(self):
        assert menu.is_valid_range(3, 2) is True

    def test_step3_invalid_negative(self, capsys):
        assert menu.is_valid_range(3, -1) is False
        assert "ERROR" in capsys.readouterr().out

    def test_step3_invalid_three(self, capsys):
        assert menu.is_valid_range(3, 3) is False

    def test_step4_valid_min(self):
        assert menu.is_valid_range(4, 0) is True

    def test_step4_valid_max(self):
        assert menu.is_valid_range(4, 2) is True

    def test_step4_invalid_negative(self, capsys):
        assert menu.is_valid_range(4, -1) is False
        assert "ERROR" in capsys.readouterr().out

    def test_step4_invalid_three(self, capsys):
        assert menu.is_valid_range(4, 3) is False


class TestSelectCarType:
    def test_select_sedan_updates_global_and_prints(self, capsys):
        menu.select_car_type(1)
        assert menu.q0 == 1
        assert "Sedan" in capsys.readouterr().out

    def test_select_suv_updates_global_and_prints(self, capsys):
        menu.select_car_type(2)
        assert menu.q0 == 2
        assert "SUV" in capsys.readouterr().out

    def test_select_truck_updates_global_and_prints(self, capsys):
        menu.select_car_type(3)
        assert menu.q0 == 3
        assert "Truck" in capsys.readouterr().out


class TestSelectEngine:
    def test_select_gm(self, capsys):
        menu.select_engine(1)
        assert menu.q1 == 1
        assert "GM" in capsys.readouterr().out

    def test_select_toyota(self, capsys):
        menu.select_engine(2)
        assert menu.q1 == 2
        assert "TOYOTA" in capsys.readouterr().out

    def test_select_wia(self, capsys):
        menu.select_engine(3)
        assert menu.q1 == 3
        assert "WIA" in capsys.readouterr().out

    def test_select_broken_engine(self, capsys):
        menu.select_engine(4)
        assert menu.q1 == 4
        assert "고장난 엔진" in capsys.readouterr().out


class TestSelectBrake:
    def test_select_mando(self, capsys):
        menu.select_brake(1)
        assert menu.q2 == 1
        assert "MANDO" in capsys.readouterr().out

    def test_select_continental(self, capsys):
        menu.select_brake(2)
        assert menu.q2 == 2
        assert "CONTINENTAL" in capsys.readouterr().out

    def test_select_bosch(self, capsys):
        menu.select_brake(3)
        assert menu.q2 == 3
        assert "BOSCH" in capsys.readouterr().out


class TestSelectSteering:
    def test_select_bosch(self, capsys):
        menu.select_steering(1)
        assert menu.q3 == 1
        assert "BOSCH" in capsys.readouterr().out

    def test_select_mobis(self, capsys):
        menu.select_steering(2)
        assert menu.q3 == 2
        assert "MOBIS" in capsys.readouterr().out


class TestBuildCar:
    def test_all_zeros_returns_car_with_none_fields(self):
        car = menu._build_car()
        assert car.car_type is None
        assert car.engine is None
        assert car.brake is None
        assert car.steering is None

    def test_sedan_gm_mando_bosch(self):
        menu.q0, menu.q1, menu.q2, menu.q3 = 1, 1, 1, 1
        car = menu._build_car()
        assert car.car_type == CarType.SEDAN
        assert car.engine == Engine.GM
        assert car.brake == Brake.MANDO
        assert car.steering == Steering.BOSCH_S

    def test_suv_toyota_continental_mobis(self):
        menu.q0, menu.q1, menu.q2, menu.q3 = 2, 2, 2, 2
        car = menu._build_car()
        assert car.car_type == CarType.SUV
        assert car.engine == Engine.TOYOTA
        assert car.brake == Brake.CONTINENTAL
        assert car.steering == Steering.MOBIS

    def test_truck_wia_bosch_bosch(self):
        menu.q0, menu.q1, menu.q2, menu.q3 = 3, 3, 3, 1
        car = menu._build_car()
        assert car.car_type == CarType.TRUCK
        assert car.engine == Engine.WIA
        assert car.brake == Brake.BOSCH_B
        assert car.steering == Steering.BOSCH_S

    def test_broken_engine_maps_correctly(self):
        menu.q0, menu.q1, menu.q2, menu.q3 = 1, 4, 1, 1
        car = menu._build_car()
        assert car.engine == Engine.BROKEN


class TestShowRunResult:
    def test_compatible_car_shows_car_details_and_runs(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 1, 1, 1, 1  # Sedan+GM+MANDO+BOSCH_S
        menu.show_run_result()
        out = capsys.readouterr().out
        assert "Sedan" in out
        assert "GM" in out
        assert "Mando" in out
        assert "Bosch" in out
        assert "동작됩니다" in out

    def test_incompatible_car_shows_not_running(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 1, 1, 2, 2  # Sedan+GM+CONTINENTAL+MOBIS
        menu.show_run_result()
        assert "동작되지 않습니다" in capsys.readouterr().out

    def test_broken_engine_shows_engine_failure(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 1, 4, 1, 1  # Sedan+BROKEN+MANDO+BOSCH_S
        menu.show_run_result()
        out = capsys.readouterr().out
        assert "고장" in out
        assert "움직이지 않습니다" in out

    def test_truck_gm_bosch_bosch_runs(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 3, 1, 3, 1  # Truck+GM+BOSCH_B+BOSCH_S
        menu.show_run_result()
        out = capsys.readouterr().out
        assert "Truck" in out
        assert "동작됩니다" in out

    def test_suv_toyota_incompatible(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 2, 2, 1, 1  # SUV+TOYOTA+MANDO+BOSCH_S
        menu.show_run_result()
        assert "동작되지 않습니다" in capsys.readouterr().out


class TestShowTestResult:
    def test_compatible_car_shows_pass(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 1, 1, 1, 1  # Sedan+GM+MANDO+BOSCH_S
        menu.show_test_result()
        assert "PASS" in capsys.readouterr().out

    def test_incompatible_car_shows_fail_message(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 1, 1, 2, 2  # Sedan+GM+CONTINENTAL+MOBIS
        menu.show_test_result()
        assert "FAIL" in capsys.readouterr().out

    def test_toyota_suv_shows_fail(self, capsys):
        menu.q0, menu.q1, menu.q2, menu.q3 = 2, 2, 1, 1  # SUV+TOYOTA+MANDO+BOSCH_S
        menu.show_test_result()
        assert "FAIL" in capsys.readouterr().out


class TestRun:
    def _run(self, inputs):
        with patch("builtins.input", side_effect=inputs), \
             patch("ui.menu.delay"), \
             patch("ui.menu.clear"):
            menu.run()

    def test_exit_quits_immediately(self, capsys):
        self._run(["exit"])
        assert "바이바이" in capsys.readouterr().out

    def test_non_numeric_input_shows_error(self, capsys):
        self._run(["abc", "exit"])
        out = capsys.readouterr().out
        assert "ERROR" in out
        assert "숫자" in out

    def test_out_of_range_at_step0_shows_error(self, capsys):
        self._run(["9", "exit"])
        assert "ERROR" in capsys.readouterr().out

    def test_full_flow_run_with_valid_car(self, capsys):
        # Sedan → GM → MANDO → BOSCH_S → RUN → exit
        self._run(["1", "1", "1", "1", "1", "exit"])
        assert "동작됩니다" in capsys.readouterr().out

    def test_full_flow_test_with_valid_car(self, capsys):
        # Sedan → GM → MANDO → BOSCH_S → Test → exit
        self._run(["1", "1", "1", "1", "2", "exit"])
        assert "PASS" in capsys.readouterr().out

    def test_full_flow_run_with_incompatible_car(self, capsys):
        # Sedan → GM → CONTINENTAL → MOBIS → RUN → exit
        self._run(["1", "1", "2", "2", "1", "exit"])
        assert "동작되지 않습니다" in capsys.readouterr().out

    def test_full_flow_run_with_broken_engine(self, capsys):
        # Sedan → BROKEN → MANDO → BOSCH_S → RUN → exit
        self._run(["1", "4", "1", "1", "1", "exit"])
        assert "고장" in capsys.readouterr().out

    def test_full_flow_test_with_incompatible_car(self, capsys):
        # Sedan → GM → CONTINENTAL → MOBIS → Test → exit
        self._run(["1", "1", "2", "2", "2", "exit"])
        assert "FAIL" in capsys.readouterr().out

    def test_back_at_step4_returns_to_step0(self, capsys):
        # Complete car → 0 (back to step 0) → exit
        self._run(["1", "1", "1", "1", "0", "exit"])
        capsys.readouterr()

    def test_back_at_step1_returns_to_step0(self, capsys):
        # Sedan → 0 (back to step 0) → exit
        self._run(["1", "0", "exit"])
        capsys.readouterr()

    def test_back_at_step2_returns_to_step1(self, capsys):
        # Sedan → GM → 0 (back to engine) → TOYOTA → MANDO → BOSCH_S → exit
        self._run(["1", "1", "0", "2", "1", "1", "exit"])
        capsys.readouterr()

    def test_back_at_step3_returns_to_step2(self, capsys):
        # Sedan → GM → MANDO → 0 (back to brake) → BOSCH_B → BOSCH_S → exit
        self._run(["1", "1", "1", "0", "3", "1", "exit"])
        capsys.readouterr()

    def test_invalid_range_at_step1_shows_error(self, capsys):
        self._run(["1", "9", "exit"])
        assert "ERROR" in capsys.readouterr().out

    def test_invalid_range_at_step2_shows_error(self, capsys):
        self._run(["1", "1", "9", "exit"])
        assert "ERROR" in capsys.readouterr().out

    def test_invalid_range_at_step3_shows_error(self, capsys):
        self._run(["1", "1", "1", "9", "exit"])
        assert "ERROR" in capsys.readouterr().out

    def test_invalid_range_at_step4_shows_error(self, capsys):
        self._run(["1", "1", "1", "1", "9", "exit"])
        assert "ERROR" in capsys.readouterr().out


class TestMain:
    def test_main_executes_run_when_invoked_as_main(self):
        with patch("builtins.input", return_value="exit"), \
             patch("ui.menu.delay"), \
             patch("ui.menu.clear"):
            runpy.run_module("main", run_name="__main__", alter_sys=False)
