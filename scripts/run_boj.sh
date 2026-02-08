#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <problem_id>"
  echo "Example: $0 2562"
  exit 1
fi

problem_id="$1"
root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
problem_dir="$root_dir/boj/$problem_id"
main_py="$problem_dir/main.py"

if [[ ! -f "$main_py" ]]; then
  echo "main.py not found: $main_py"
  exit 1
fi

if command -v python >/dev/null 2>&1; then
  py_cmd="python"
else
  py_cmd="python3"
fi

run_case() {
  local input_file="$1"
  local base_name
  base_name="$(basename "$input_file")"
  local suffix="${base_name#input}"
  local expected_file="$problem_dir/output${suffix}"

  echo ""
  echo "[CASE] $base_name"

  local actual_file
  actual_file="$(mktemp)"
  "$py_cmd" "$main_py" < "$input_file" > "$actual_file"

  echo "[OUTPUT]"
  cat "$actual_file"

  if [[ -f "$expected_file" ]]; then
    echo "[EXPECT] $(basename "$expected_file")"
    if diff -u "$expected_file" "$actual_file" >/dev/null; then
      echo "[RESULT] PASS"
    else
      echo "[RESULT] FAIL"
      echo "[DIFF]"
      diff -u "$expected_file" "$actual_file" || true
    fi
  else
    echo "[RESULT] output 파일이 없어 비교는 생략"
  fi

  rm -f "$actual_file"
}

# input.txt 우선 처리
if [[ -f "$problem_dir/input.txt" ]]; then
  run_case "$problem_dir/input.txt"
fi

# input1.txt, input2.txt ... 처리
shopt -s nullglob
for input_file in "$problem_dir"/input[0-9]*.txt; do
  run_case "$input_file"
done
shopt -u nullglob

# 입력 파일이 전혀 없으면 표준입력 모드
if [[ ! -f "$problem_dir/input.txt" ]] && compgen -G "$problem_dir/input[0-9]*.txt" >/dev/null; then
  :
elif [[ ! -f "$problem_dir/input.txt" ]]; then
  echo "input 파일이 없어 표준입력 모드로 실행합니다."
  "$py_cmd" "$main_py"
fi
