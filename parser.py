import pandas as pd
from valve import Valve
import os

def parse_devices_from_spreadsheet(filepath, plc_io):
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext in [".xlsm", ".xlsx"]:
        df = pd.read_excel(filepath)
    elif ext == ".csv":
        df = pd.read_csv(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    valve_map = {}

    for _, row in df.iterrows():
        tag = str(row.get("Tag Name", "")).strip()
        desc = str(row.get("DESCRIPTION", "")).strip().lower()
        io_tag = str(row.get("PLCIO Tags", "")).strip()

        if not tag.startswith(("XV", "V")) or not io_tag or desc == "nan":
            if desc == "nan":
                print(f"[WARN] {tag}: Description is 'nan', skipping.")
            continue

        base_tag = tag[:6]  # Adjust if needed

        if base_tag not in valve_map:
            valve_map[base_tag] = {"name": base_tag}

        if "open feedback" in desc:
            valve_map[base_tag]["open_fb_tag"] = io_tag
        elif "closed feedback" in desc:
            valve_map[base_tag]["close_fb_tag"] = io_tag
        elif desc == "open":
            valve_map[base_tag]["open_tag"] = io_tag

    valves = []
    for tag, cfg in valve_map.items():
        if all(k in cfg for k in ("open_tag", "open_fb_tag", "close_fb_tag")):
            valves.append(Valve(cfg["name"], cfg["open_tag"], cfg["open_fb_tag"], cfg["close_fb_tag"], plc_io))
        else:
            print(f"[SKIP] Incomplete valve definition for {tag}: {cfg}")

    return {"valves": valves}