#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Reset iOS Simulators
# @raycast.mode compact
# @raycast.packageName Leo Dev
# @raycast.icon 📱
# @raycast.needsConfirmation true

xcrun simctl shutdown all 2>/dev/null
xcrun simctl erase all && echo "All simulators erased"
