#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Meeting Mode
# @raycast.mode silent
# @raycast.packageName Leo Dev
# @raycast.icon 🎙️

AS=/opt/homebrew/bin/aerospace
$AS move-workspace-to-monitor --workspace s 'DELL S2725QS' 'DELL' 'main'
open -a Granola
$AS workspace s
$AS workspace z
echo "Meeting mode on"
