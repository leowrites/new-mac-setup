#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Kill Port
# @raycast.mode compact
# @raycast.packageName Leo Dev
# @raycast.icon 🔪
# @raycast.argument1 { "type": "text", "placeholder": "Port", "percentEncoded": false }

PIDS="$(lsof -ti "tcp:$1" -sTCP:LISTEN)"
if [ -z "$PIDS" ]; then
  echo "Nothing listening on $1"
  exit 0
fi
NAMES="$(ps -o comm= -p $PIDS | xargs -n1 basename | sort -u | tr '\n' ' ')"
kill $PIDS
sleep 1
STILL="$(lsof -ti "tcp:$1" -sTCP:LISTEN)"
[ -n "$STILL" ] && kill -9 $STILL
echo "Killed ${NAMES% } on $1"
