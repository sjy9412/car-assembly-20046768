import assemble
import pytest
from unittest.mock import patch


def reset_globals():
    assemble.q0 = 0
    assemble.q1 = 0
    assemble.q2 = 0
    assemble.q3 = 0


# ──────────────────────────────────────────────
# is_valid_range()
# ──────────────────────────────────────────────

class TestIsValidRange:
    def setup_method(self):
        reset_globals()

    # step 0 : 차량 타입 (유효 1~3)
    def test_car_type_valid(self):
        assert assemble.is_valid_range(0, 1) is True
        assert assemble.is_valid_range(0, 2) is True
        assert assemble.is_valid_range(0, 3) is True

    def test_car_type_below_min(self):
        assert assemble.is_valid_range(0, 0) is False

    def test_car_type_above_max(self):
        assert assemble.is_valid_range(0, 4) is False

    # step 1 : 엔진 (유효 0~4, 0=뒤로가기)
    def test_engine_valid_all(self):
        for v in range(0, 5):
            assert assemble.is_valid_range(1, v) is True

    def test_engine_above_max(self):
        assert assemble.is_valid_range(1, 5) is False

    def test_engine_below_min(self):
        assert assemble.is_valid_range(1, -1) is False

    # step 2 : 제동장치 (유효 0~3, 0=뒤로가기)
    def test_brake_valid_all(self):
        for v in range(0, 4):
            assert assemble.is_valid_range(2, v) is True

    def test_brake_above_max(self):
        assert assemble.is_valid_range(2, 4) is False

    def test_brake_below_min(self):
        assert assemble.is_valid_range(2, -1) is False

    # step 3 : 조향장치 (유효 0~2, 0=뒤로가기)
    def test_steering_valid_all(self):
        for v in range(0, 3):
            assert assemble.is_valid_range(3, v) is True

    def test_steering_above_max(self):
        assert assemble.is_valid_range(3, 3) is False

    def test_steering_below_min(self):
        assert assemble.is_valid_range(3, -1) is False

    # step 4 : Run/Test (유효 0~2)
    def test_run_test_valid_all(self):
        for v in range(0, 3):
            assert assemble.is_valid_range(4, v) is True

    def test_run_test_above_max(self):
        assert assemble.is_valid_range(4, 3) is False

    def test_run_test_below_min(self):
        assert assemble.is_valid_range(4, -1) is False


# ──────────────────────────────────────────────
# is_valid_check() — 5가지 호환성 규칙
# ──────────────────────────────────────────────

class TestIsValidCheck:
    def setup_method(self):
        reset_globals()

    # 규칙 1: BOSCH 제동장치 → BOSCH 조향장치 필수
    def test_bosch_brake_requires_bosch_steering_fail(self):
        assemble.q2 = assemble.BOSCH_B
        assemble.q3 = assemble.MOBIS        # BOSCH 아님
        assert assemble.is_valid_check() is False

    def test_bosch_brake_with_bosch_steering_pass(self):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.BOSCH_B
        assemble.q3 = assemble.BOSCH_S
        assert assemble.is_valid_check() is True

    # 규칙 2: Continental 제동장치 → Sedan 불가
    def test_continental_sedan_fail(self):
        assemble.q0 = assemble.SEDAN
        assemble.q2 = assemble.CONTINENTAL
        assert assemble.is_valid_check() is False

    def test_continental_suv_pass(self):
        assemble.q0 = assemble.SUV
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.CONTINENTAL
        assemble.q3 = assemble.BOSCH_S
        assert assemble.is_valid_check() is True

    # 규칙 3: TOYOTA 엔진 → SUV 불가
    def test_toyota_suv_fail(self):
        assemble.q0 = assemble.SUV
        assemble.q1 = assemble.TOYOTA
        assert assemble.is_valid_check() is False

    def test_toyota_sedan_pass(self):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = assemble.TOYOTA
        assemble.q2 = assemble.MANDO
        assemble.q3 = assemble.BOSCH_S
        assert assemble.is_valid_check() is True

    # 규칙 4: WIA 엔진 → Truck 불가
    def test_wia_truck_fail(self):
        assemble.q0 = assemble.TRUCK
        assemble.q1 = assemble.WIA
        assert assemble.is_valid_check() is False

    def test_wia_sedan_pass(self):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = assemble.WIA
        assemble.q2 = assemble.MANDO
        assemble.q3 = assemble.BOSCH_S
        assert assemble.is_valid_check() is True

    # 규칙 5: MANDO 제동장치 → Truck 불가
    def test_mando_truck_fail(self):
        assemble.q0 = assemble.TRUCK
        assemble.q2 = assemble.MANDO
        assert assemble.is_valid_check() is False

    def test_mando_sedan_pass(self):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.MANDO
        assemble.q3 = assemble.BOSCH_S
        assert assemble.is_valid_check() is True

    # 모든 규칙을 통과하는 정상 조합
    def test_fully_valid_combination(self):
        assemble.q0 = assemble.TRUCK
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.BOSCH_B
        assemble.q3 = assemble.BOSCH_S
        assert assemble.is_valid_check() is True


# ──────────────────────────────────────────────
# select_*() — 전역 변수에 올바른 값이 저장되는지
# ──────────────────────────────────────────────

class TestSelectFunctions:
    def setup_method(self):
        reset_globals()

    def test_select_car_type_sedan(self, capsys):
        assemble.select_car_type(assemble.SEDAN)
        assert assemble.q0 == assemble.SEDAN
        assert "Sedan" in capsys.readouterr().out

    def test_select_car_type_suv(self, capsys):
        assemble.select_car_type(assemble.SUV)
        assert assemble.q0 == assemble.SUV
        assert "SUV" in capsys.readouterr().out

    def test_select_car_type_truck(self, capsys):
        assemble.select_car_type(assemble.TRUCK)
        assert assemble.q0 == assemble.TRUCK
        assert "Truck" in capsys.readouterr().out

    def test_select_engine_gm(self, capsys):
        assemble.select_engine(assemble.GM)
        assert assemble.q1 == assemble.GM
        assert "GM" in capsys.readouterr().out

    def test_select_engine_toyota(self, capsys):
        assemble.select_engine(assemble.TOYOTA)
        assert assemble.q1 == assemble.TOYOTA
        assert "TOYOTA" in capsys.readouterr().out

    def test_select_engine_wia(self, capsys):
        assemble.select_engine(assemble.WIA)
        assert assemble.q1 == assemble.WIA
        assert "WIA" in capsys.readouterr().out

    def test_select_engine_broken(self, capsys):
        assemble.select_engine(4)
        assert assemble.q1 == 4
        assert "고장" in capsys.readouterr().out

    def test_select_brake_mando(self, capsys):
        assemble.select_brake(assemble.MANDO)
        assert assemble.q2 == assemble.MANDO
        assert "MANDO" in capsys.readouterr().out

    def test_select_brake_continental(self, capsys):
        assemble.select_brake(assemble.CONTINENTAL)
        assert assemble.q2 == assemble.CONTINENTAL
        assert "CONTINENTAL" in capsys.readouterr().out

    def test_select_brake_bosch(self, capsys):
        assemble.select_brake(assemble.BOSCH_B)
        assert assemble.q2 == assemble.BOSCH_B
        assert "BOSCH" in capsys.readouterr().out

    def test_select_steering_bosch(self, capsys):
        assemble.select_steering(assemble.BOSCH_S)
        assert assemble.q3 == assemble.BOSCH_S
        assert "BOSCH" in capsys.readouterr().out

    def test_select_steering_mobis(self, capsys):
        assemble.select_steering(assemble.MOBIS)
        assert assemble.q3 == assemble.MOBIS
        assert "MOBIS" in capsys.readouterr().out


# ──────────────────────────────────────────────
# delay()
# ──────────────────────────────────────────────

class TestDelay:
    @patch("time.sleep")
    def test_delay_converts_ms_to_seconds(self, mock_sleep):
        assemble.delay(800)
        mock_sleep.assert_called_once_with(0.8)

    @patch("time.sleep")
    def test_delay_zero(self, mock_sleep):
        assemble.delay(0)
        mock_sleep.assert_called_once_with(0.0)


# ──────────────────────────────────────────────
# show_menu()
# ──────────────────────────────────────────────

class TestShowMenu:
    @patch("assemble.clear")
    def test_show_menu_step0(self, _mock_clear, capsys):
        assemble.show_menu(0)
        out = capsys.readouterr().out
        assert "Sedan" in out
        assert "SUV" in out
        assert "Truck" in out

    @patch("assemble.clear")
    def test_show_menu_step1(self, _mock_clear, capsys):
        assemble.show_menu(1)
        out = capsys.readouterr().out
        assert "GM" in out
        assert "TOYOTA" in out
        assert "WIA" in out
        assert "고장난 엔진" in out

    @patch("assemble.clear")
    def test_show_menu_step2(self, _mock_clear, capsys):
        assemble.show_menu(2)
        out = capsys.readouterr().out
        assert "MANDO" in out
        assert "CONTINENTAL" in out
        assert "BOSCH" in out

    @patch("assemble.clear")
    def test_show_menu_step3(self, _mock_clear, capsys):
        assemble.show_menu(3)
        out = capsys.readouterr().out
        assert "BOSCH" in out
        assert "MOBIS" in out

    @patch("assemble.clear")
    def test_show_menu_step4(self, _mock_clear, capsys):
        assemble.show_menu(4)
        out = capsys.readouterr().out
        assert "RUN" in out
        assert "Test" in out


# ──────────────────────────────────────────────
# run_produced_car()
# ──────────────────────────────────────────────

class TestRunProducedCar:
    def setup_method(self):
        reset_globals()

    def test_incompatible_combination_does_not_run(self, capsys):
        assemble.q0 = assemble.SEDAN
        assemble.q2 = assemble.CONTINENTAL
        assemble.run_produced_car()
        assert "동작되지 않습니다" in capsys.readouterr().out

    def test_broken_engine_does_not_run(self, capsys):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = 4              # 고장난 엔진
        assemble.q2 = assemble.MANDO
        assemble.q3 = assemble.BOSCH_S
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "고장" in out
        assert "움직이지 않습니다" in out

    def test_sedan_gm_mando_bosch_runs(self, capsys):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.MANDO
        assemble.q3 = assemble.BOSCH_S
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "Sedan" in out
        assert "GM" in out
        assert "Mando" in out
        assert "Bosch" in out
        assert "동작됩니다" in out

    def test_suv_toyota_continental_mobis_blocked(self, capsys):
        # TOYOTA + SUV 규칙 위반
        assemble.q0 = assemble.SUV
        assemble.q1 = assemble.TOYOTA
        assemble.q2 = assemble.CONTINENTAL
        assemble.q3 = assemble.MOBIS
        assemble.run_produced_car()
        assert "동작되지 않습니다" in capsys.readouterr().out

    def test_truck_gm_bosch_bosch_runs(self, capsys):
        assemble.q0 = assemble.TRUCK
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.BOSCH_B
        assemble.q3 = assemble.BOSCH_S
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "Truck" in out
        assert "GM" in out
        assert "Bosch" in out
        assert "동작됩니다" in out

    def test_sedan_wia_continental_bosch_runs(self, capsys):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = assemble.WIA
        assemble.q2 = assemble.BOSCH_B
        assemble.q3 = assemble.BOSCH_S
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "WIA" in out
        assert "동작됩니다" in out

    def test_suv_gm_continental_mobis_runs(self, capsys):
        assemble.q0 = assemble.SUV
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.CONTINENTAL
        assemble.q3 = assemble.MOBIS
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "SUV" in out
        assert "Continental" in out
        assert "Mobis" in out
        assert "동작됩니다" in out


# ──────────────────────────────────────────────
# test_produced_car()
# ──────────────────────────────────────────────

class TestTestProducedCar:
    def setup_method(self):
        reset_globals()

    def test_continental_sedan_fail(self, capsys):
        assemble.q0 = assemble.SEDAN
        assemble.q2 = assemble.CONTINENTAL
        assemble.test_produced_car()
        assert "FAIL" in capsys.readouterr().out

    def test_toyota_suv_fail(self, capsys):
        assemble.q0 = assemble.SUV
        assemble.q1 = assemble.TOYOTA
        assemble.test_produced_car()
        assert "FAIL" in capsys.readouterr().out

    def test_wia_truck_fail(self, capsys):
        assemble.q0 = assemble.TRUCK
        assemble.q1 = assemble.WIA
        assemble.test_produced_car()
        assert "FAIL" in capsys.readouterr().out

    def test_mando_truck_fail(self, capsys):
        assemble.q0 = assemble.TRUCK
        assemble.q2 = assemble.MANDO
        assemble.test_produced_car()
        assert "FAIL" in capsys.readouterr().out

    def test_bosch_brake_non_bosch_steering_fail(self, capsys):
        assemble.q2 = assemble.BOSCH_B
        assemble.q3 = assemble.MOBIS
        assemble.test_produced_car()
        assert "FAIL" in capsys.readouterr().out

    def test_valid_combination_pass(self, capsys):
        assemble.q0 = assemble.SEDAN
        assemble.q1 = assemble.GM
        assemble.q2 = assemble.MANDO
        assemble.q3 = assemble.BOSCH_S
        assemble.test_produced_car()
        assert "PASS" in capsys.readouterr().out
