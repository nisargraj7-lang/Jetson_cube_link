# Jetson ↔ Cube Orange+ link (companion computer, MAVLink over USB)

Bench-verified procedure for connecting a Jetson Orin Nano (JetPack 6.x, Ubuntu 22.04)
to a Cube Orange+ running ArduCopter 4.7.x. **Props off for all bench work.**

## Per-drone IDs
Set `MAV_SYSID` on each Cube (Mission Planner → CONFIG → Full Parameter List).
(In ArduCopter 4.7 the old name `SYSID_THISMAV` is `MAV_SYSID`.)

| Drone  | Hostname | MAV_SYSID |
|--------|----------|-----------|
| ISR-1  | isr1     | 1 |
| ISR-2  | isr2     | 2 |
| ISR-3  | isr3     | 3 |
| MARK-1 | mark1    | 4 |
| DROP-1 | drop1    | 5 |
| SPARE  | spare    | 6 |

Write params, then reboot the Cube. Only one computer can use the Cube's USB at a time
(close Mission Planner before testing from the Jetson).

## Laptop → Jetson (SSH over the USB-C link)
```
ssh <jetson-user>@192.168.55.1
```
If Windows shows "Unidentified network" on the Jetson adapter, set a static IP on it:
`192.168.55.100`, mask `255.255.255.0`, no gateway/DNS.

## On the Jetson
```bash
# 1. Is the Cube visible?
lsusb
ls /dev/ttyACM*
ls -l /dev/serial/by-id/

# 2. Install tools in an isolated environment
sudo apt install -y python3-venv python3-pip
python3 -m venv ~/mavenv
source ~/mavenv/bin/activate
pip install pymavlink pyserial

# 3. Serial permission, then log out/in
sudo usermod -aG dialout $USER
exit
# (ssh back in)  then:  groups   # must include dialout

# 4. Heartbeat test (read-only)
source ~/mavenv/bin/activate
python3 check_heartbeat.py
```
Or run `bash setup_cube_link.sh` for steps 1–3.

Expected: `Heartbeat from system 1 component 1`, `type 2`, `autopilot 3`, `LINK OK`.

## Troubleshooting
- No `/dev/ttyACM*`: Cube unpowered or charge-only cable.
- `Permission denied`: log out/in after `usermod`; check `groups`.
- No heartbeat: try `/dev/ttyACM1`; close Mission Planner.

## Final-drone wiring (TELEM2, more vibration-tolerant than USB)
Jetson pin 8 → Cube RX, pin 10 → Cube TX, pin 6 → GND (no 5 V). Cube params:
`SERIAL2_PROTOCOL=2`, `SERIAL2_BAUD=921`. Test:
`python3 check_heartbeat.py /dev/ttyTHS1 921600`
