#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Pull All Repos
# @raycast.mode fullOutput
# @raycast.packageName Leo Dev
# @raycast.icon ⬇️

source "$HOME/.config/raycast/leo/lib/repos.sh"
for r in $ALL_REPOS; do
  dir="$(repo_path "$r")"
  [ -d "$dir/.git" ] || { printf '%-18s not cloned\n' "$r"; continue; }
  branch="$(git -C "$dir" branch --show-current)"
  git -C "$dir" fetch --quiet --prune 2>/dev/null || { printf '%-18s fetch failed\n' "$r"; continue; }
  if [ "$branch" != "main" ] && [ "$branch" != "master" ]; then
    printf '%-18s fetched only (on %s)\n' "$r" "$branch"
  elif [ -n "$(git -C "$dir" status --porcelain)" ]; then
    printf '%-18s fetched only (local changes)\n' "$r"
  elif out="$(git -C "$dir" merge --ff-only --quiet "@{u}" 2>&1)"; then
    printf '%-18s up to date on %s\n' "$r" "$branch"
  else
    printf '%-18s could not fast-forward: %s\n' "$r" "$out"
  fi
done
