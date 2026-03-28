# Result Ledger Template

연속 연구는 **누적 비교 가능한 기록**이 핵심입니다.

## Minimal markdown table

```md
| round | hypothesis | change | hard gates | metric | evidence | status | next step | notes |
|---|---|---|---|---|---|---|---|---|
| 0 | baseline | none | pass | ... | baseline snapshot | keep | choose first hypothesis | baseline |
| 1 | ... | ... | pass/fail | ... | log/link/table | keep/discard/crash/... | ... | ... |
```

## TSV template

탭 구분 형식을 쓰면 후처리가 쉽습니다.

```text
round	hypothesis	change	hard_gates	metric	evidence	status	next_step	notes
0	baseline	none	pass	...	baseline snapshot	keep	choose first hypothesis	baseline
1	...	...	pass	...	log/link/table	discard	...	...
```

## Status vocabulary

- `keep` — 현재 best state로 채택
- `discard` — baseline 또는 직전 best보다 못함
- `crash` — 실행 실패 또는 가설 붕괴
- `pivot` — 접근 방향 전환
- `rescope` — 계약 또는 범위를 다시 씀
- `escalate` — 사람 판단 또는 별도 reviewer가 필요함
- `stop` — 종료

## End-of-loop summary

마지막에는 아래를 꼭 남깁니다.

```md
## Final summary
- objective:
- best state:
- biggest gain:
- failed lines of inquiry:
- remaining risks:
- stop reason:
- next recommended experiment:
```

## Optional state snapshot

여러 세션에 걸친 루프라면 ledger와 별도로 아래도 유지합니다.

```md
## State Snapshot
- baseline:
- best-known state:
- active hypothesis:
- most recent decision:
- open risks:
- next candidates:
```
