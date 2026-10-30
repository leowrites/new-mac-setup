#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Open PR for Current Branch
# @raycast.mode silent
# @raycast.packageName Leo Dev
# @raycast.icon 🔀
# @raycast.argument1 { "type": "dropdown", "placeholder": "Repo", "data": [{"title": "wallet", "value": "wallet"}, {"title": "micro-svc", "value": "micro-svc"}, {"title": "wallet-core", "value": "wallet-core"}, {"title": "credible", "value": "credible"}, {"title": "terraform", "value": "terraform"}, {"title": "isomdl", "value": "isomdl"}, {"title": "sprucekit-mobile", "value": "sprucekit-mobile"}, {"title": "sprucetree", "value": "sprucetree"}, {"title": "tamga", "value": "tamga"}] }

export PATH="/opt/homebrew/bin:$PATH"
source "$HOME/.config/raycast/leo/lib/repos.sh"
require_repo "$1"
cd "$REPO_DIR"
BRANCH="$(git branch --show-current)"
if gh pr view --web >/dev/null 2>&1; then
  echo "Opened PR for $BRANCH"
else
  echo "No PR for $BRANCH in $1"
  exit 1
fi
