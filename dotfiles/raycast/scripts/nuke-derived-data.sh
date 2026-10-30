#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Nuke Xcode DerivedData
# @raycast.mode compact
# @raycast.packageName Leo Dev
# @raycast.icon 🧨
# @raycast.needsConfirmation true

DD="$HOME/Library/Developer/Xcode/DerivedData"
[ -d "$DD" ] || { echo "No DerivedData folder"; exit 0; }
SIZE="$(du -sh "$DD" | cut -f1)"
find "${DD:?}" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
echo "Cleared DerivedData ($SIZE)"
