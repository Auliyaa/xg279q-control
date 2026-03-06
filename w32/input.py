#!/usr/bin/env python3

import argparse
import time
from monitorcontrol import get_monitors, Monitor, InputSource

MON_DELAY = 0.2


def find_monitor(id: str) -> Monitor:
    print("Scanning monitors...")
    for i, monitor in enumerate(get_monitors()):
        print(f"Checking monitor {i}...")
        try:
            with monitor:
                time.sleep(MON_DELAY)
                caps = monitor.get_vcp_capabilities()
                print("Capabilities:", caps)
                if id in caps.get("model", ""):
                    print("Target monitor found.")
                    return monitor
        except Exception as e:
            print("Error reading monitor:", e)
            continue
    return None


def get_input_source(mon: Monitor) -> int:
    time.sleep(MON_DELAY)
    return mon.get_input_source()


def set_input_source(mon: Monitor, id: int):
    time.sleep(MON_DELAY)
    mon.set_input_source(id)


def main():
    print("Script started.")
    parser = argparse.ArgumentParser(description="Switch monitor input source.")
    parser.add_argument(
        "--input",
        choices=["dp1", "hdmi1", "hdmi2"],
        required=True,
    )
    args = parser.parse_args()

    print("Requested input:", args.input)

    monitor = find_monitor("XG279")
    if not monitor:
        print("Monitor not found.")
        return

    print("Opening monitor context...")
    with monitor:
        current = get_input_source(monitor)
        print(f"Current input source: {current}")

        mapping = {
            "dp1": InputSource.DP1,
            "hdmi1": InputSource.HDMI1,
            "hdmi2": InputSource.HDMI2,
        }

        print("Switching input...")
        set_input_source(monitor, mapping[args.input])
        print("Switch complete.")


if __name__ == "__main__":
    main()
