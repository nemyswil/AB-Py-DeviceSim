import pandas as pd
from valve import Valve

class MockPLC:
    def __init__(self):
        self.tags = {}  # dictionary to hold simulated tag values

    def read_tag(self, tag):
        return self.tags.get(tag, False)

    def write_tag(self, tag, value):
        self.tags[tag] = value
        print(f"[PLC WRITE] {tag} = {value}")

def load_valves_from_excel(file_path, plc_io):
    df = pd.read_excel(file_path)
    valves = []
    for _, row in df.iterrows():
        valve = Valve(
            row["Name"],
            row["openTag"],
            row["openFeedbackTag"],
            row["closeFeedbackTag"],
            plc_io
        )
        valves.append(valve)
    return valves