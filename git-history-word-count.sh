#!/usr/bin/env bash
set -e

# Count total words in markdown files for each point in time of a Git repository

dir="${1}"

if [[ -z "${dir}" ]]; then
  echo "pass path to a Git directory"
  exit 1
fi

cd "${dir}"
origbranch="$(git rev-parse --abbrev-ref HEAD)"

run() {
  line="$1"
  hash="$(echo "${line}" | cut -c -7)"
  msg="$(echo "${line}" | cut -c 9-)"
  git checkout -q ${hash}
  count="$(find . -name '*.md' | xargs -I{} cat "{}" | wc -w)"
  echo "${count} words at ${hash} (${msg})"
  git checkout -q ${origbranch}
}

commits="$(git log --pretty=oneline --abbrev-commit | cat -n | sort -nr | cut -c 8-)"
echo "${commits}" | while read line; do run "${line}"; done