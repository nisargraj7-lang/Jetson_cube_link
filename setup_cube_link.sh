#!/usr/bin/env bash
# Jetson Orin Nano <-> Cube Orange+ MAVLink link setup (USB), per-drone.
# Run ON the Jetson (as your normal user, not root). Props OFF for all bench work.
# Usage: bash setup_cube_link.sh
set -e

echo "== 1. Check the Cube is visible over USB =="
lsusb | grep -i -E "cubepilot|ardupilot" || echo "WARNING: Cube not detected. Check power and a USB DATA cable."
ls /dev/ttyACM* 2>/dev/null || echo "WARNING: no /dev/ttyACM* port found."
ls -l /dev/serial/by-id/ 2>/dev/null || true

echo "== 2. Install Python venv tools (does not touch system Python packages) =="
sudo apt install -y python3-venv python3-pip

echo "== 3. Create isolated environment with pymavlink =="
python3 -m venv ~/mavenv
source ~/mavenv/bin/activate
pip install pymavlink pyserial

echo "== 4. Allow this user to use serial ports =="
sudo usermod -aG dialout "$USER"
echo "NOTE: log out and back in (exit, then ssh again) so the dialout group applies."
echo "Done. Next: python3 check_heartbeat.py"
