# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# 프로그램 실행
python main.py

# 가상 환경 활성화 (Windows)
.venv\Scripts\activate

# 테스트 실행
pytest tests/ -v

# 커버리지 포함 테스트
pytest tests/ -v --cov=. --cov-report=term-missing
```

## Architecture

Python 3.13 CLI 애플리케이션.

**의존성:** `pytest`, `pytest-cov` (테스트 전용, `.venv` 내 설치됨)

### 디렉토리 구조

```
car_assembly/
├── main.py              # CLI 진입점 (ui.menu.run() 호출)
├── models/
│   ├── parts.py         # CarType / Engine / Brake / Steering IntEnum 정의
│   └── car.py           # Car dataclass (is_complete, reset)
├── services/
│   ├── compatibility.py # CompatibilityRule / CompatibilityResult / RULES / check_compatibility
│   └── assembler.py     # Assembler 클래스 (validate, can_run)
├── ui/
│   └── menu.py          # 모든 입출력 처리 및 조립 흐름 제어 (run())
└── tests/
    ├── test_models.py
    ├── test_compatibility.py
    └── test_assembler.py
```

### 모델 (`models/`)

- `parts.py` — `CarType`, `Engine`, `Brake`, `Steering` 을 `IntEnum`으로 정의. 정수 상수와 호환되므로 기존 코드와 혼용 가능.
- `car.py` — `Car` dataclass. 4개 부품 필드(`car_type`, `engine`, `brake`, `steering`)를 `Optional`로 보유. `is_complete()` / `reset()` 메서드 제공.

### 서비스 (`services/`)

- `compatibility.py` — 호환성 검증 전담. `RULES` 리스트에 5가지 규칙을 `CompatibilityRule` dataclass로 보유. `check_compatibility(car)` 가 `Car` 객체를 받아 `CompatibilityResult`(is_compatible, message) 반환.
- `assembler.py` — `Assembler` 클래스. `validate(car)` 는 호환성 검증, `can_run(car)` 는 고장난 엔진 + 호환성을 통합 판단.

### UI (`ui/`)

- `menu.py` — 모든 `print()` / `input()` 처리 담당. 전역 변수(`q0`~`q3`)로 조립 단계별 선택값을 유지. `run()` 함수가 이벤트 루프 진입점.

| 변수 | 역할 | 선택값 |
|------|------|--------|
| `q0` | 차량 타입 | SEDAN(1) / SUV(2) / TRUCK(3) |
| `q1` | 엔진 | GM(1) / TOYOTA(2) / WIA(3) / 고장난 엔진(4) |
| `q2` | 제동장치 | MANDO(1) / CONTINENTAL(2) / BOSCH_B(3) |
| `q3` | 조향장치 | BOSCH_S(1) / MOBIS(2) |

### 조립 흐름

`run()` 이벤트 루프 → 입력 수신 → `is_valid_range()` 검증 → 각 `select_*()` 함수로 상태 저장 → 스텝 4에서 `show_run_result()` / `show_test_result()` 호출.

입력 `0`은 이전 단계로 돌아가는 뒤로가기이고, `exit` 입력 시 종료한다.

### 호환성 검증 규칙

`services/compatibility.py`의 `RULES`에 정의되며, `ui/menu.py`는 `check_compatibility()` / `Assembler`를 통해 이 규칙을 사용한다.

1. **Continental 제동장치 → Sedan 불가**
2. **TOYOTA 엔진 → SUV 불가**
3. **WIA 엔진 → Truck 불가**
4. **MANDO 제동장치 → Truck 불가**
5. **Bosch 제동장치 → Bosch 조향장치 필수** (타사 호환 불가)
