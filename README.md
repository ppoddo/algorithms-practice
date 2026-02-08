# algorithms-practice

개인 알고리즘 코드 작성/테스트용 저장소입니다.

## Workspace setting
`cd dokidoki-dockerize && code study-folder.code-workspace` 로 열기

## Python setup (WSL)
WSL(Ubuntu)에서 `python` 명령이 없으면 아래처럼 설치합니다.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python-is-python3

python --version
python3 --version
```

## Structure
- `boj/<problem_id>/main.py`: 백준 제출 코드
- `boj/<problem_id>/input.txt`: 테스트 입력 1개일 때
- `boj/<problem_id>/input1.txt`, `input2.txt`...: 테스트 입력 여러 개일 때
- `boj/<problem_id>/output.txt`: `input.txt`의 기대 출력
- `boj/<problem_id>/output1.txt`, `output2.txt`...: 각 입력의 기대 출력
- `programmers/<problem_id>/solution.py`: 프로그래머스 제출 코드
- `programmers/<problem_id>/main.py`: 로컬 실행용 테스트 엔트리(선택)
- `scripts/run_boj.sh`: 백준 로컬 실행/검증 도우미
- `scripts/run_programmers.sh`: 프로그래머스 로컬 실행/검증 도우미
- `scripts/sync_to_fork.sh`: 포크 레포 구조 변환 도우미(커밋/푸시 없음)

## Workflow
1. 선정된 문제의 플랫폼/번호로 폴더를 만듭니다.
2. 폴더에 `input.txt`와 코드 파일(`main.py` 또는 `solution.py`)을 준비합니다.
3. 문제를 풉니다.
4. 플랫폼에 맞는 스크립트로 로컬 실행/검증합니다.
5. 출력 검증이 끝나면 사이트에 제출합니다. (BaekjoonHub 설치/연결 확인)
6. 정답이면 BaekjoonHub가 `fork-algorithms-study`에 원본 폴더를 생성합니다.
7. 로컬 `fork-algorithms-study`에서 `origin/main`을 최신화하고, `upstream/main` 기준으로 PR 브랜치를 새로 만듭니다.
8. `sync_to_fork.sh`로 PR용 표준 경로(`archive/<platform>/<problem_id>/<user_id>`)로 복사합니다.
9. `git add archive/...`만 수행해 `백준/`, `프로그래머스/` 원본 폴더는 PR에 포함하지 않습니다.
10. 커밋/푸시 후 GitHub에서 `DokiDokiStudy/Algorithms-study`로 PR을 생성합니다.

## Command Examples

```bash
# BOJ 실행
./scripts/run_boj.sh 9012

# Programmers 실행
./scripts/run_programmers.sh 12906

# 포크 저장소 이동
cd fork-algorithms-study

# 최신화
git fetch origin
git fetch upstream
git checkout main
git pull origin main

# PR 브랜치 생성(중요: upstream/main 기준)
git checkout -b pr/batch-2026-02 upstream/main

# PR용 구조 변환
cd ..
./scripts/sync_to_fork.sh boj 9012 ppoddo
./scripts/sync_to_fork.sh programmers 12906 ppoddo

# PR 브랜치에서 archive만 커밋
cd fork-algorithms-study
git add archive/boj/9012/ppoddo archive/programmers/12906/ppoddo
git commit -m "[BOJ-9012][PGS-12906] ppoddo 풀이 추가"
git push -u origin pr/batch-2026-02
```

## Run (BOJ)

```bash
./scripts/run_boj.sh 2562
```

동작 방식:
- `input.txt`가 있으면 실행
- `input1.txt`, `input2.txt` ... 가 있으면 모두 순회 실행
- 매 케이스마다 대응되는 `output*.txt`가 있으면 `PASS/FAIL` 비교 출력

## Run (Programmers)

```bash
./scripts/run_programmers.sh 12906
```

동작 방식:
- `main.py`가 있으면 우선 실행
- `main.py`가 없으면 `solution.py`로 fallback 실행
- `input*.txt`/`output*.txt` 패턴으로 케이스 실행/비교

## Sync to Fork (No Commit)

플랫폼에 맞는 BaekjoonHub 원본 폴더에서 파일 2개를 그대로 복사합니다.

- `README.md`
- 코드 파일 1개(예: `최댓값.py`, `같은_숫자는_싫어.py`)

대상 경로:
- `archive/<platform>/<problem_id>/<user_id>/`

```bash
# 백준
./scripts/sync_to_fork.sh boj 2562 ppoddo

# 프로그래머스
./scripts/sync_to_fork.sh programmers 12906 ppoddo
```

옵션:

```bash
# 실제 반영 없이 확인
./scripts/sync_to_fork.sh --dry-run boj 2562 ppoddo

# 포크 저장소 경로가 기본값과 다를 때
./scripts/sync_to_fork.sh --fork-dir ./fork-algorithms-study programmers 12906 ppoddo
```

주의:
- 이 스크립트는 **commit/push를 자동으로 하지 않습니다.**
- 변환 후 포크 저장소에서 내용을 검토한 뒤 수동으로 commit/push/PR 하세요.

## Troubleshooting
- `python: command not found`
  - `python-is-python3` 설치 후 새 셸에서 다시 실행
- `Permission denied: ./scripts/run_boj.sh`
  - `chmod +x scripts/run_boj.sh scripts/run_programmers.sh`
- `main.py not found`
  - 문제 번호 경로 확인: `boj/<problem_id>/main.py`
