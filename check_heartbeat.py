#!/usr/bin/env python3
"""Read-only MAVLink heartbeat check between the Jetson and the Cube.
Sends NO commands to the vehicle. Safe on the bench.

Usage:
    source ~/mavenv/bin/activate
    python3 check_heartbeat.py [port] [baud]
Defaults: /dev/ttyACM0 115200 (USB). For the wired TELEM2 link use: /dev/ttyTHS1 921600
"""
import sys
from pymavlink import mavutil

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
baud = int(sys.argv[2]) if len(sys.argv) > 2 else 115200

m = mavutil.mavlink_connection(port, baud=baud)
if m.wait_heartbeat(timeout=10) is None:
    sys.exit(f"No heartbeat on {port} @ {baud}. Check cable, power, port, permissions.")

msg = m.recv_match(type="HEARTBEAT", blocking=True, timeout=5)
print(f"Heartbeat from system {msg.get_srcSystem()} component {msg.get_srcComponent()}")
print(f"type {msg.type} (2 = quadrotor), autopilot {msg.autopilot} (3 = ArduPilot)")
print("LINK OK")
