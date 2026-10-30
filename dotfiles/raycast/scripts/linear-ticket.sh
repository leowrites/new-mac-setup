#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Linear Ticket
# @raycast.mode silent
# @raycast.packageName Leo Dev
# @raycast.icon 📋
# @raycast.argument1 { "type": "text", "placeholder": "CAMV-674 or 674" }

ID="$(echo "$1" | tr '[:lower:]' '[:upper:]' | tr -d ' ')"
[[ "$ID" =~ ^[0-9]+$ ]] && ID="CAMV-$ID"
open "https://linear.app/spruceid/issue/$ID"
