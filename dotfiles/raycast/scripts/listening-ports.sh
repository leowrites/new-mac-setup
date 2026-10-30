#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Listening Ports
# @raycast.mode fullOutput
# @raycast.packageName Leo Dev
# @raycast.icon 🔌
# @raycast.argument1 { "type": "dropdown", "placeholder": "Show", "optional": true, "data": [{"title": "Dev servers", "value": "dev"}, {"title": "Everything", "value": "all"}] }

printf '%-7s %-8s %-18s %s\n' PORT PID PROCESS FOLDER
lsof -nP -a -iTCP -sTCP:LISTEN -u "$(id -u)" -Fpcn 2>/dev/null | awk '
  /^p/ { pid = substr($0, 2) }
  /^c/ { cmd = substr($0, 2) }
  /^n/ { n = split($0, a, ":"); print a[n], pid, cmd }
' | sort -n -u | while read -r port pid cmd; do
  cwd="$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | awk '/^n/ { print substr($0, 2) }')"
  if [ "${1:-dev}" = "dev" ]; then
    case "$cwd" in
      / | "$HOME/Library"* | /opt/homebrew/var*) continue ;;
    esac
  fi
  printf '%-7s %-8s %-18s %s\n' "$port" "$pid" "$cmd" "${cwd/#$HOME/~}"
done
