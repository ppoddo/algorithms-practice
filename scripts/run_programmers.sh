#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <problem_id>"
  echo "Example: $0 12906"
  exit 1
fi

problem_id="$1"
root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
problem_dir="$root_dir/programmers/$problem_id"
main_py="$problem_dir/main.py"
solution_py="$problem_dir/solution.py"

if [[ ! -f "$main_py" ]] && [[ ! -f "$solution_py" ]]; then
  echo "Neither main.py nor solution.py found in: $problem_dir"
  exit 1
fi

if command -v python >/dev/null 2>&1; then
  py_cmd="python"
else
  py_cmd="python3"
fi

entry_py="$main_py"
if [[ ! -f "$entry_py" ]]; then
  entry_py="$solution_py"
  echo "main.py not found; fallback to solution.py"
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
  "$py_cmd" "$entry_py" < "$input_file" > "$actual_file"

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

ran_any=0

if [[ -f "$problem_dir/input.txt" ]]; then
  run_case "$problem_dir/input.txt"
  ran_any=1
fi

shopt -s nullglob
for input_file in "$problem_dir"/input[0-9]*.txt; do
  run_case "$input_file"
  ran_any=1
done
shopt -u nullglob

if [[ "$ran_any" -eq 0 ]]; then
  echo "input 파일이 없어 엔트리 파일을 바로 실행합니다: $(basename "$entry_py")"
  "$py_cmd" "$entry_py"
fi
