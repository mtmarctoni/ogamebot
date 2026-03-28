import json
import os
from datetime import datetime, timezone
from typing import Optional
from config.types import EmpireSnapshotDict
from config.config import DB_SNAPSHOTS_PATH

def save_empire_snapshot(empire_data: EmpireSnapshotDict, filename: Optional[str] = None) -> None:
    """Save the latest empire snapshot to a JSON file inside the data folder."""
    timestamp_str = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    snapshot: EmpireSnapshotDict = {
        "timestamp": timestamp_str,
        "planets": empire_data['planets']
    }

    # Save with timestamped filename
    ts_filename = f"empire_snapshot_{timestamp_str.replace(':', '').replace('-', '').replace('.', '')}.json"
    ts_path = os.path.join(DB_SNAPSHOTS_PATH, ts_filename)
    os.makedirs(DB_SNAPSHOTS_PATH, exist_ok=True)
    with open(ts_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    # Also save/overwrite empire_snapshot_latest.json
    latest_path = os.path.join(DB_SNAPSHOTS_PATH, "empire_snapshot_latest.json")
    with open(latest_path, "w") as f:
        json.dump(snapshot, f, indent=2)