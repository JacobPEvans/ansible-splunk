#!/usr/bin/env bash
#
# Run every template unit test in tests/templates/.
#
# Discovery is by glob, deliberately. The CI workflow used to name each test
# file by hand, and that list had drifted: five test files existed in the
# directory and were never invoked, among them the guard added to catch a
# comment welding itself into a rendered search value. A test CI never runs is
# not a check at all, and nothing reports its absence.
#
# Every test is run even after one fails, so a single failure does not hide the
# rest; the script exits non-zero if any failed.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

failed=0
ran=0

for t in tests/templates/test_*.py; do
  [ -e "$t" ] || continue
  ran=$((ran + 1))
  printf '::group::%s\n' "$t"
  if python3 "$t"; then
    :
  else
    printf '::error::%s failed\n' "$t"
    failed=1
  fi
  printf '::endgroup::\n'
done

if [ "$ran" -eq 0 ]; then
  echo "::error::no template tests were discovered - the glob matched nothing"
  exit 1
fi

echo "ran ${ran} template test(s)"
exit "$failed"
