#!/usr/bin/python3
import os
import re
import shutil
import subprocess
import sys

CONFIG = os.path.expanduser("~/.aerospace.toml")
AEROSPACE = shutil.which("aerospace") or "/opt/homebrew/bin/aerospace"

UNMANAGED_WORKSPACES = {"1", "2", "3", "4"}

HOME_SCREENS = {
    "w": ["DELL S2725QC", "DELL", "main"],
    "i": ["DELL S2725QS", "DELL", "main"],
    "t": ["DELL S2725QC", "DELL", "main"],
    "z": ["DELL S2725QC", "DELL", "main"],
    "s": ["built-in", "main"],
    "d": ["built-in", "main"],
}


def aerospace(*args):
    result = subprocess.run([AEROSPACE, *args], capture_output=True, text=True)
    return result.stdout.strip()


def parse_value(raw):
    raw = raw.strip()
    if raw.startswith("["):
        return [a or b for a, b in re.findall(r"'([^']*)'|\"([^\"]*)\"", raw)]
    if raw in ("true", "false"):
        return raw == "true"
    return raw.strip("'\"")


def parse_config(text):
    rules = []
    assignments = {}
    section = None
    for line in text.splitlines():
        line = re.sub(r"(^|\s)#.*$", "", line).strip()
        if not line:
            continue
        if line == "[[on-window-detected]]":
            section = "rule"
            rules.append({})
            continue
        if line.startswith("["):
            section = "assign" if line == "[workspace-to-monitor-force-assignment]" else None
            continue
        if "=" not in line:
            continue
        key, raw = line.split("=", 1)
        key = key.strip().strip("'\"")
        if section == "rule":
            rules[-1][key] = parse_value(raw)
        elif section == "assign":
            value = parse_value(raw)
            assignments[key] = value if isinstance(value, list) else [value]
    return rules, assignments


def matches(rule, window):
    checks = [
        ("if.app-id", lambda v: v == window["app_id"]),
        ("if.app-name-regex-substring", lambda v: re.search(v, window["app_name"], re.I)),
        ("if.window-title-regex-substring", lambda v: re.search(v, window["title"], re.I)),
    ]
    if rule.get("if.during-aerospace-startup"):
        return False
    return all(test(rule[key]) for key, test in checks if key in rule)


def apply(command, window_id):
    name, _, arg = command.partition(" ")
    if name == "layout":
        aerospace("layout", "--window-id", window_id, *arg.split())
    elif name == "move-node-to-workspace":
        aerospace("move-node-to-workspace", "--window-id", window_id, arg.strip())


def list_windows():
    out = aerospace(
        "list-windows", "--all", "--format",
        "%{window-id}\t%{workspace}\t%{app-bundle-id}\t%{app-name}\t%{window-title}",
    )
    windows = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 5:
            windows.append(dict(zip(("id", "workspace", "app_id", "app_name", "title"), parts)))
    return windows


def main():
    with open(CONFIG) as f:
        rules, assignments = parse_config(f.read())

    focused = aerospace("list-windows", "--focused", "--format", "%{window-id}")

    for window in list_windows():
        if window["workspace"] in UNMANAGED_WORKSPACES:
            continue
        for rule in rules:
            if not matches(rule, window):
                continue
            run = rule.get("run", [])
            for command in run if isinstance(run, list) else [run]:
                apply(command, window["id"])
            if not rule.get("check-further-callbacks"):
                break

    for workspace in aerospace("list-workspaces", "--monitor", "all", "--empty", "no").splitlines():
        aerospace("flatten-workspace-tree", "--workspace", workspace)
        tiled = aerospace(
            "list-windows", "--workspace", workspace, "--format", "%{window-id}\t%{window-layout}"
        )
        for line in tiled.splitlines():
            window_id, layout = line.split("\t")
            if layout != "floating":
                aerospace("layout", "--window-id", window_id, "accordion")
                break
        aerospace("balance-sizes", "--workspace", workspace)

    for workspace, monitors in {**HOME_SCREENS, **assignments}.items():
        aerospace("move-workspace-to-monitor", "--workspace", workspace, *monitors)

    if focused:
        aerospace("focus", "--window-id", focused)


if __name__ == "__main__":
    sys.exit(main())
