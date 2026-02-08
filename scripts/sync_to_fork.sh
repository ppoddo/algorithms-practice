#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/sync_to_fork.sh [--dry-run] [--fork-dir <path>] <platform> <problem_id> <user_id>

Examples:
  ./scripts/sync_to_fork.sh boj 2562 ppoddo
  ./scripts/sync_to_fork.sh programmers 12906 ppoddo
  ./scripts/sync_to_fork.sh --dry-run boj 2562 ppoddo
  ./scripts/sync_to_fork.sh --fork-dir ./fork-algorithms-study programmers 12906 alice

Behavior:
  - Reads raw files from BaekjoonHub folders
  - Copies raw README.md and source file as-is
  - Target: <fork>/archive/<platform>/<problem_id>/<user_id>/
  - Does NOT commit or push
USAGE
}

dry_run=0
fork_dir_override=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --fork-dir)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --fork-dir"
        usage
        exit 1
      fi
      fork_dir_override="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -ne 3 ]]; then
  usage
  exit 1
fi

platform_input="$1"
problem_id="$2"
user_id="$3"

case "$platform_input" in
  boj|baekjoon)
    platform="boj"
    raw_root="백준"
    ;;
  programmers|pgs)
    platform="programmers"
    raw_root="프로그래머스"
    ;;
  *)
    echo "Unsupported platform: $platform_input"
    echo "Use one of: boj, baekjoon, programmers, pgs"
    exit 1
    ;;
esac

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -n "$fork_dir_override" ]]; then
  fork_dir="$fork_dir_override"
  if [[ "$fork_dir" != /* ]]; then
    fork_dir="$root_dir/$fork_dir"
  fi
else
  fork_dir="$root_dir/fork-algorithms-study"
fi

if [[ ! -d "$fork_dir/.git" ]]; then
  echo "Fork repository not found: $fork_dir"
  echo "Check fork path or pass --fork-dir"
  exit 1
fi

shopt -s nullglob
raw_candidates=("$fork_dir/$raw_root"/*/"$problem_id".* "$fork_dir/$raw_root"/"$problem_id".*)
shopt -u nullglob

if [[ ${#raw_candidates[@]} -eq 0 ]]; then
  echo "Raw directory not found for platform=$platform problem_id=$problem_id"
  echo "Expected pattern: $fork_dir/$raw_root/*/$problem_id.*"
  exit 1
fi

if [[ ${#raw_candidates[@]} -gt 1 ]]; then
  echo "Multiple raw directories found. Pass one path manually by cleanup then retry:"
  for d in "${raw_candidates[@]}"; do
    echo "  - $d"
  done
  exit 1
fi

raw_dir="${raw_candidates[0]}"
raw_readme="$raw_dir/README.md"

if [[ ! -f "$raw_readme" ]]; then
  echo "README.md not found in raw directory: $raw_dir"
  exit 1
fi

shopt -s nullglob
source_candidates=("$raw_dir"/*)
shopt -u nullglob

code_count=0
code_file=""
for f in "${source_candidates[@]}"; do
  if [[ -f "$f" ]] && [[ "$(basename "$f")" != "README.md" ]]; then
    code_file="$f"
    code_count=$((code_count + 1))
  fi
done

if [[ $code_count -eq 0 ]]; then
  echo "No source file found in raw directory: $raw_dir"
  exit 1
fi

if [[ $code_count -gt 1 ]]; then
  echo "Multiple source files found. Keep one and retry:"
  for f in "${source_candidates[@]}"; do
    if [[ -f "$f" ]] && [[ "$(basename "$f")" != "README.md" ]]; then
      echo "  - $f"
    fi
  done
  exit 1
fi

dest_dir="$fork_dir/archive/$platform/$problem_id/$user_id"
dest_readme="$dest_dir/README.md"
dest_code="$dest_dir/$(basename "$code_file")"

mkdir -p "$dest_dir"

echo "Platform: $platform"
echo "Raw dir: $raw_dir"
echo "Copy: $raw_readme -> $dest_readme"
echo "Copy: $code_file -> $dest_code"

if [[ "$dry_run" -eq 1 ]]; then
  echo "[DRY-RUN] No files written"
  exit 0
fi

cp "$raw_readme" "$dest_readme"
cp "$code_file" "$dest_code"

echo ""
echo "Done"
echo "- $dest_readme"
echo "- $dest_code"
echo ""
echo "Next steps (manual):"
echo "  1) cd $fork_dir"
echo "  2) git status"
echo "  3) git add archive/$platform/$problem_id/$user_id"
echo "  4) git commit && git push && create PR"
