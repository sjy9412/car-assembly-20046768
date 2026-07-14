# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# 프로그램 실행
python assemble.py

# 가상 환경 활성화 (Windows)
.venv\Scripts\activate
```

## Architecture

단일 파일(`assemble.py`) Python 3.13 CLI 애플리케이션. 외부 의존성 없음.

### 상태 관리

전역 변수(`q0`~`q4`)로 조립 단계별 선택값을 유지한다.

| 변수 | 단계 | 선택값 |
|------|------|--------|
| `q0` | 진행 단계 (0~4) | 현재 스텝 |
| `q1` | 차량 타입 | SEDAN(1) / SUV(2) / TRUCK(3) |
| `q2` | 엔진 | GM(1) / TOYOTA(2) / WIA(3) |
| `q3` | 제동장치 | MANDO(1) / CONTINENTAL(2) / BOSCH_B(3) |
| `q4` | 조향장치 | BOSCH_S(1) / MOBIS(2) |

### 조립 흐름

`main()` 이벤트 루프 → 입력 수신 → `is_valid_range()` 검증 → 각 `select_*()` 함수로 상태 저장 → 스텝 4에서 `run_produced_car()` / `test_produced_car()` 호출.

입력 `0`은 이전 단계로 돌아가는 뒤로가기이고, `exit` 입력 시 종료한다.

### 호환성 검증 규칙 (`is_valid_check()`)

1. **Bosch 제동장치 → Bosch 조향장치 필수** (타사 호환 불가)
2. **Continental 제동장치 → Sedan 불가**
3. **TOYOTA 엔진 → SUV 불가**
4. **WIA 엔진 → Truck 불가**
5. **MANDO 제동장치 → Truck 불가**

### 코드 구조

- **상수 (6~31줄):** 단계 식별자 및 부품 코드
- **유틸 (33~39줄):** `delay()`, `clear()`
- **메뉴/입력 (41~100줄):** `show_menu()`, `is_valid_range()`
- **선택 저장 (102~141줄):** `select_car_type()`, `select_engine()`, `select_brake()`, `select_steering()`
- **검증/실행 (142~204줄):** `is_valid_check()`, `run_produced_car()`, `test_produced_car()`
- **메인 루프 (206~259줄):** `main()`

## 코드 스타일

PyCharm Black formatter 설정 적용됨.
