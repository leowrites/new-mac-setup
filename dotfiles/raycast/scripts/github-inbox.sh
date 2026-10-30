#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title GitHub Inbox
# @raycast.mode fullOutput
# @raycast.packageName Leo Dev
# @raycast.icon 📬

export PATH="/opt/homebrew/bin:$PATH"
FMT='.[] | "  \(.repository.name)#\(.number)  \(.title)\n    \(.url)"'

echo "Waiting on my review"
gh search prs --review-requested=@me --state=open --json repository,number,title,url --jq "$FMT"
echo
echo "My open PRs"
gh search prs --author=@me --state=open --json repository,number,title,url --jq "$FMT"
