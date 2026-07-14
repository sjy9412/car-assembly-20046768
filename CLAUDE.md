# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# 프로그램 실행
python assemble.py

# 가상 환경 활성화 (Windows)
.venv\Scripts\activate

# 테스트 실행 (Step 1 이후)
pytest tests/ -v
```

## Architecture

단일 파일(`assemble.py`) Python 3.13 CLI 애플리케이션. 외부 의존성 없음.

### 상태 관리

전역 변수(`q0`~`q3`)로 조립 단계별 선택값을 유지한다. (`q4`는 미사용)

| 변수 | 역할 | 선택값 |
|------|------|--------|
| `q0` | 차량 타입 | SEDAN(1) / SUV(2) / TRUCK(3) |
| `q1` | 엔진 | GM(1) / TOYOTA(2) / WIA(3) / 고장난 엔진(4) |
| `q2` | 제동장치 | MANDO(1) / CONTINENTAL(2) / BOSCH_B(3) |
| `q3` | 조향장치 | BOSCH_S(1) / MOBIS(2) |

### 조립 흐름

`main()` 이벤트 루프 → 입력 수신 → `is_valid_range()` 검증 → 각 `select_*()` 함수로 상태 저장 → 스텝 4에서 `run_produced_car()` / `test_produced_car()` 호출.

입력 `0`은 이전 단계로 돌아가는 뒤로가기이고, `exit` 입력 시 종료한다.

### 호환성 검증 규칙 (`is_valid_check()`)

1. **Bosch 제동장치 → Bosch 조향장치 필수** (타사 호환 불가)
2. **Continental 제동장치 → Sedan 불가**
3. **TOYOTA 엔진 → SUV 불가**
4. **WIA 엔진 → Truck 불가**
5. **MANDO 제동장치 → Truck 불가**

동일한 규칙이 `is_valid_check()`와 `test_produced_car()` 두 곳에 중복 구현되어 있다.

## Refactoring

리팩토링 계획은 `PLAN.md` 참조. Test-First 전략으로 5단계 진행.

- Step 1: 테스트 기준선 작성 (현재 코드 기준 pytest)
- Step 2: 안전성 수정 (bare except, 하드코딩 상수, 미사용 변수)
- Step 3: OOP 전환 (Enum + dataclass)
- Step 4: 서비스 계층 도입 (호환성 규칙 통합)
- Step 5: UI 분리 및 최종 구조 완성

