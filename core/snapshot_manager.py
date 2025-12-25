import json
import os
from typing import Optional
from config.types import EmpireSnapshotDict

def save_empire_snapshot(snapshot: EmpireSnapshotDict, filename: Optional[str] = None) -> None:
    """Save the latest empire snapshot to a JSON file inside the data folder."""
    if filename is None:
        filename = os.path.join("data", "empire_snapshot.json")
    else:
        filename = os.path.join("data", filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(snapshot, f, indent=2)