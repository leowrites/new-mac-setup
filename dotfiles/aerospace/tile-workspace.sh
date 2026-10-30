#!/bin/bash
AS=/opt/homebrew/bin/aerospace
for id in $($AS list-windows --workspace focused --format '%{window-id}'); do
  $AS layout --window-id "$id" tiling
done
$AS balance-sizes
