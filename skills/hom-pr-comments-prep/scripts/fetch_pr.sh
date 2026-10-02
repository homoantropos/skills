#!/usr/bin/env bash
# Fetch a PR's metadata, review threads and comments as JSON.
# Usage: fetch_pr.sh <PR URL | PR number>   (a bare number uses the repo in the current directory)
set -euo pipefail

arg="${1:?Usage: fetch_pr.sh <PR URL | PR number>}"

if [[ "$arg" =~ github\.com/([^/]+)/([^/]+)/pull/([0-9]+) ]]; then
  owner="${BASH_REMATCH[1]}"; name="${BASH_REMATCH[2]}"; number="${BASH_REMATCH[3]}"
elif [[ "$arg" =~ ^#?([0-9]+)$ ]]; then
  number="${BASH_REMATCH[1]}"
  owner="$(gh repo view --json owner -q .owner.login)"
  name="$(gh repo view --json name -q .name)"
else
  echo "Not a PR URL or number: $arg" >&2; exit 2
fi

gh api graphql -F owner="$owner" -F name="$name" -F number="$number" -f query='
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      title
      body
      url
      reviewThreads(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          isResolved
          isOutdated
          path
          line
          originalLine
          comments(first: 50) {
            pageInfo { hasNextPage }
            nodes { author { __typename login } body diffHunk }
          }
        }
      }
      reviews(first: 100) { pageInfo { hasNextPage } nodes { author { __typename login } body } }
      comments(first: 100) { pageInfo { hasNextPage } nodes { author { __typename login } body } }
    }
  }
}'
