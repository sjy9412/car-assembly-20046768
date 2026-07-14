# Car Assembly 리팩토링 계획서

## 현황 요약

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.13 |
| 소스 파일 | `assemble.py` 1개 (261줄) |
| 외부 의존성 | 없음 |
| 테스트 | 없음 |

---

## 문제점

| 분류 | 문제 |
|------|------|
| 절차지향 구조 | 전역 변수(`q0~q4`)로 상태 관리, 함수마다 `global` 선언으로 직접 수정 |
| 중복 로직 | 호환성 검증 규칙이 `is_valid_check()`와 `test_produced_car()` 두 곳에 중복 구현 |
| 안전하지 않은 문법 | `except:` bare except 사용, 상수와 하드코딩 값 혼용, 미사용 변수 `q4` |
| 확장성 없음 | 부품 하나 추가 시 7곳 수정 필요 |
| 테스트 없음 | 전역 상태 의존 구조로 단위 테스트 작성 불가 |

---

## 리팩토링 전략

테스트를 가장 먼저 작성하여 현재 동작을 고정(freeze)한 뒤,  
각 단계마다 테스트 통과를 확인하며 순차적으로 개선한다.

---

## Step 1: 테스트 기준선 작성

**목표:** 현재 코드의 동작을 pytest 테스트로 고정한다.

- `pytest` 설치
- `tests/` 디렉토리 생성
- 아래 3개 영역에 대한 테스트 작성
  - `is_valid_range()` — 단계별 입력 범위 검증 (유효/경계/초과 케이스)
  - `is_valid_check()` — 5가지 호환성 규칙 전부 (불가 케이스 + 정상 케이스)
  - `select_*()` 함수 — 전역 변수에 올바른 값이 저장되는지 확인
- 전역 변수는 각 테스트의 `setup_method`에서 초기화하여 테스트 간 상태 오염 방지

**완료 기준:** `pytest tests/` 전체 PASSED

---

## Step 2: 안전성 수정

**목표:** Step 1 테스트를 유지하면서 코드 안전 문제만 수정한다.

- `except:` → `except ValueError:` 로 변경
- `run_produced_car()` 내 하드코딩 숫자 비교를 기존 상수(`SEDAN`, `SUV` 등)로 통일
- 미사용 변수 `q4` 삭제
- 오류 메시지와 실제 허용 범위 일치시키기 (예: 엔진 단계에서 0이 유효함을 메시지에 반영)
- 전체 함수에 타입 힌팅 추가

**완료 기준:** Step 1 테스트 전체 PASSED 유지

---

## Step 3: OOP 전환 — 모델 클래스 도입

**목표:** 전역 변수를 객체로 대체한다.

- `models/parts.py` — `Enum`으로 `CarType`, `Engine`, `Brake`, `Steering` 정의
- `models/car.py` — `dataclass`로 `Car` 정의 (`car_type`, `engine`, `brake`, `steering` 필드)
- `Car.is_complete()` — 4개 부품이 모두 선택되었는지 반환
- `Car.reset()` — 전체 선택 초기화
- `tests/test_models.py` 추가 — `Car` 완성/미완성/초기화 케이스 테스트

**완료 기준:** 기존 테스트 + `test_models.py` 전체 PASSED

---

## Step 4: 서비스 계층 도입 — 호환성 규칙 통합

**목표:** 두 곳에 중복된 검증 로직을 단일 데이터 구조로 통합한다.

- `services/compatibility.py`
  - `CompatibilityRule` — 규칙 하나를 표현하는 데이터 클래스 (설명문 + 조건 필드)
  - `RULES` — 5가지 호환성 규칙을 담은 리스트
  - `check_compatibility(car)` — `Car` 객체를 받아 `CompatibilityResult` 반환
  - `is_valid_check()` / `test_produced_car()` 의 중복 로직을 이 함수 하나로 대체
- `services/assembler.py`
  - `Assembler` 클래스 — `validate()` (호환성 검증), `can_run()` (고장난 엔진 + 호환성 통합 판단)
- `tests/test_compatibility.py` 추가 — 5가지 불가 규칙 + 정상 케이스
- `tests/test_assembler.py` 추가 — 고장난 엔진, 비호환 조합, 정상 조합
- `assemble.py`의 `is_valid_check()` / `test_produced_car()`를 서비스 호출로 교체
- 레거시 `tests/test_assemble.py` 삭제

**완료 기준:** `test_compatibility.py` + `test_assembler.py` 전체 PASSED, 레거시 테스트 삭제 완료

---

## Step 5: UI 분리 및 최종 구조 완성

**목표:** 입출력과 비즈니스 로직을 완전히 분리한다.

- `ui/menu.py` — 모든 `print()` / `input()` 처리 담당
- `main.py` — 진입점, `ui/`와 `services/`만 orchestrate
- `services/` 계층은 `ui/`를 import하지 않음
- `assemble.py` 제거

**최종 디렉토리 구조:**

```
car_assembly/
├── main.py
├── models/
│   ├── __init__.py
│   ├── parts.py
│   └── car.py
├── services/
│   ├── __init__.py
│   ├── compatibility.py
│   └── assembler.py
├── ui/
│   ├── __init__.py
│   └── menu.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_compatibility.py
    └── test_assembler.py
```

**완료 기준:** 전체 테스트 PASSED + `python main.py` 실행 동작 확인

---

## 진행 흐름 요약

```
Step 1  테스트 기준선 작성   현재 코드(전역 변수) 기준 pytest 작성
  ↓
Step 2  안전성 수정          bare except, 하드코딩 상수, 미사용 변수, 타입 힌팅
  ↓
Step 3  OOP 전환             Enum + dataclass 도입, 전역 변수 제거
  ↓
Step 4  서비스 계층 도입     중복 검증 로직 통합, Assembler 클래스
  ↓
Step 5  UI 분리              menu.py 분리, main.py 진입점 교체
```
