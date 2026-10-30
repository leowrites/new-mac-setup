#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Copy Current Branch
# @raycast.mode silent
# @raycast.packageName Leo Dev
# @raycast.icon 🌿
# @raycast.argument1 { "type": "dropdown", "placeholder": "Repo", "data": [{"title": "wallet", "value": "wallet"}, {"title": "micro-svc", "value": "micro-svc"}, {"title": "wallet-core", "value": "wallet-core"}, {"title": "credible", "value": "credible"}, {"title": "terraform", "value": "terraform"}, {"title": "isomdl", "value": "isomdl"}, {"title": "sprucekit-mobile", "value": "sprucekit-mobile"}, {"title": "sprucetree", "value": "sprucetree"}, {"title": "tamga", "value": "tamga"}] }

source "$HOME/.config/raycast/leo/lib/repos.sh"
require_repo "$1"
BRANCH="$(git -C "$REPO_DIR" branch --show-current)"
printf '%s' "$BRANCH" | pbcopy
echo "Copied $BRANCH"
