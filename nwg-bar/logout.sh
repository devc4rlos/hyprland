#!/bin/bash
pkill -15 -f phpstorm
pkill -15 -f jetbrains-toolbox

sleep 1

hyprctl dispatch exit
