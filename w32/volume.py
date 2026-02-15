#!/usr/bin/env python3

import argparse
import time
from monitorcontrol import get_monitors, Monitor

MON_DELAY = 0.2
VCP_VOLUME = 0x62
MIN_VOL = 0
MAX_VOL = 100


def find_monitor(id: str) -> Monitor:
    for monitor in get_monitors():
        with monitor:
            time.sleep(MON_DELAY)
            try:
                caps = monitor.get_vcp_capabilities()
                if id in caps["model"]:
                    return monitor
            except Exception:
                continue
    return None


def get_volume(mon: Monitor) -> int:
    time.sleep(MON_DELAY)
    value, _ = mon.vcp.get_vcp_feature(VCP_VOLUME)
    return value


def set_volume(mon: Monitor, value: int):
    value = max(MIN_VOL, min(MAX_VOL, value))
    time.sleep(MON_DELAY)
    mon.vcp.set_vcp_feature(VCP_VOLUME, value)


def main():
    parser = argparse.ArgumentParser(description="Set monitor speaker volume.")
    parser.add_argument(
        "--volume",
        type=int,
        help="Volume level (0–100).",
        required=True,
    )
    args = parser.parse_args()

    monitor = find_monitor("XG279")
    if not monitor:
        print("Monitor not found.")
        return

    with monitor:
        current = get_volume(monitor)
        print(f"Current volume: {current}")

        set_volume(monitor, args.volume)
        print(f"Volume set to: {args.volume}")


if __name__ == "__main__":
    main()
