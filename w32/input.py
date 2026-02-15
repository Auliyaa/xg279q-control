#!/usr/bin/env python3

import argparse
import time
from monitorcontrol import get_monitors, Monitor, InputSource

MON_DELAY = 0.2

def find_monitor(id: str) -> Monitor:
    for monitor in get_monitors():
        with monitor:
            time.sleep(MON_DELAY)
            try:
                caps = monitor.get_vcp_capabilities()
                print(caps)
                if id in caps["model"]:
                    return monitor
            except Exception as e:
                print(e)
                continue
    return None

def get_input_source(mon: Monitor) -> int:
    time.sleep(MON_DELAY)
    return mon.get_input_source()

def set_input_source(mon: Monitor, id: int):
    time.sleep(MON_DELAY)
    mon.set_input_source(id)

def main():
    parser = argparse.ArgumentParser(description="Switch monitor input source.")
    parser.add_argument(
        "--input",
        choices=["dp1", "hdmi1", "hdmi2"],
        help="Input source to switch to (dp1 or hdmi2).",
        required=True,
    )
    args = parser.parse_args()

    target_input = args.input
    monitor = find_monitor("XG279")
    if not monitor:
        print("Monitor not found.")
        return

    current = get_input_source(monitor)
    print(f"Current input source: {current}")

    if target_input == "dp1":
        set_input_source(monitor, InputSource.DP1)
        print("Switched to DisplayPort 1.")
    elif target_input == "hdmi1":
        set_input_source(monitor, InputSource.HDMI1)
        print("Switched to HDMI 1.")
    elif target_input == "hdmi2":
        set_input_source(monitor, InputSource.HDMI2)
        print("Switched to HDMI 2.")

if __name__ == "__main__":
    main()
