#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Open Repo
# @raycast.mode silent
# @raycast.packageName Leo Dev
# @raycast.icon 📂
# @raycast.argument1 { "type": "dropdown", "placeholder": "Repo", "data": [{"title": "wallet", "value": "wallet"}, {"title": "micro-svc", "value": "micro-svc"}, {"title": "wallet-core", "value": "wallet-core"}, {"title": "credible", "value": "credible"}, {"title": "terraform", "value": "terraform"}, {"title": "isomdl", "value": "isomdl"}, {"title": "sprucekit-mobile", "value": "sprucekit-mobile"}, {"title": "sprucetree", "value": "sprucetree"}, {"title": "tamga", "value": "tamga"}] }
# @raycast.argument2 { "type": "dropdown", "placeholder": "In", "optional": true, "data": [{"title": "VS Code", "value": "code"}, {"title": "Ghostty", "value": "ghostty"}, {"title": "Claude Code", "value": "claude"}, {"title": "GitHub", "value": "github"}, {"title": "Finder", "value": "finder"}] }

source "$HOME/.config/raycast/leo/lib/repos.sh"
TARGET="${2:-code}"

if [ "$TARGET" = "github" ]; then
  open "https://github.com/$(repo_github "$1")"
  exit 0
fi

require_repo "$1"
case "$TARGET" in
  code) /opt/homebrew/bin/code "$REPO_DIR" ;;
  ghostty) open -na Ghostty.app --args --working-directory="$REPO_DIR" ;;
  claude) open -na Ghostty.app --args --working-directory="$REPO_DIR" -e /bin/zsh -lic claude ;;
  finder) open "$REPO_DIR" ;;
esac
echo "Opened $1"
