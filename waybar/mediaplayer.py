#!/usr/bin/env python3

import subprocess
import sys
import os

FOCUS_FILE = "/tmp/waybar_player_focus"
ICONS = {"spotify": "", "brave": "", "chrome": "", "firefox": "", "default": ""}

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    except:
        return ""

def get_players():
    p = run_cmd("playerctl -l")
    return p.split("\n") if p else []

def main():
    players = get_players()
    if not players:
        print("")
        sys.exit(0)

    focused = ""
    if os.path.exists(FOCUS_FILE):
        with open(FOCUS_FILE, "r") as f:
            focused = f.read().strip()

    if focused not in players:
        focused = players[0]
        with open(FOCUS_FILE, "w") as f:
            f.write(focused)

    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "switch":
            current_idx = players.index(focused)
            next_idx = (current_idx + 1) % len(players)
            focused = players[next_idx]
            with open(FOCUS_FILE, "w") as f:
                f.write(focused)

        elif action in ["play-pause", "next", "previous"]:
            subprocess.run(["playerctl", "-p", focused, action])

        subprocess.run(["pkill", "-RTMIN+5", "waybar"])
        if action != "switch": sys.exit(0)

    status = run_cmd(f"playerctl -p {focused} status")
    artist = run_cmd(f"playerctl -p {focused} metadata artist")
    title = run_cmd(f"playerctl -p {focused} metadata title")
    icon = next((v for k, v in ICONS.items() if k in focused.lower()), ICONS["default"])

    if status == "Playing":
        print(f"{icon}   {artist} - {title}" if title else f"{icon} {focused}")
    elif status == "Paused":
        print(f"󰏤   {artist} - {title} (Pausado)" if title else f"󰏤 {focused} (Pausado)")
        subprocess.run(["pkill", "-RTMIN+5", "waybar"])
    else:
        print(f"󰓄   {artist} - {title}" if title else f"{icon} {focused}")
        subprocess.run(["pkill", "-RTMIN+5", "waybar"])

if __name__ == "__main__":
    main()