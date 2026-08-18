"""
simulator/replay.py
-------------------
UNSW-NB15 replay/stream simulator for SentinelAI.

Continuously feeds rows from the UNSW-NB15 test dataset through the existing
ML → risk → alert → database pipeline, generating alerts automatically without
any manual API requests.

Usage
-----
    python -m simulator.replay

Environment variables
---------------------
    INTERVAL    Seconds to sleep between each flow (default: 2.0)
    MAX_FLOWS   Stop after this many flows, 0 = loop forever (default: 0)

The dataset is shuffled on each full pass so the alert stream is varied.
Both normal and attack flows are replayed to represent realistic mixed telemetry.
"""

import os
import sys
import signal
import time
import logging

import pandas as pd

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so src.* and backend.* imports work
# when the module is executed with: python -m simulator.replay
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.data_loader import load_test_data
from src.constants import DROP_COLUMNS

from backend.services.prediction_service import predict_network_flow
from backend.services.alert_service import save_alert
from backend.database.connection import SessionLocal

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [SIMULATOR] %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------
INTERVAL: float = float(os.environ.get("INTERVAL", "2.0"))
MAX_FLOWS: int = int(os.environ.get("MAX_FLOWS", "0"))

# ---------------------------------------------------------------------------
# Graceful-shutdown flag
# ---------------------------------------------------------------------------
_stop = False


def _handle_signal(signum, frame):
    global _stop
    log.info("Shutdown signal received — stopping after current flow.")
    _stop = True


signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_feature_rows() -> pd.DataFrame:
    """
    Load the UNSW-NB15 test dataset and strip the target columns so each row
    contains only the 38 features expected by predict_network_flow().
    """
    df = load_test_data()
    # Drop label / attack_cat — same columns the API request schema excludes.
    # Use errors="ignore" in case a column is already absent.
    drop = [c for c in DROP_COLUMNS if c in df.columns]
    return df.drop(columns=drop)


def _process_flow(row_dict: dict, db) -> dict:
    """
    Run one flow dict through the full pipeline and persist the resulting alert.

    Pipeline (identical to POST /predict):
        predict_network_flow()   →  ML inference + risk + alert dict
        save_alert()             →  persist to SQLite

    Returns the alert dict.
    """
    alert = predict_network_flow(row_dict)
    save_alert(db, alert)
    return alert


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run():
    global _stop
    log.info("Loading UNSW-NB15 test dataset…")
    features_df = _load_feature_rows()
    total_rows = len(features_df)
    log.info(f"Dataset loaded: {total_rows} rows  |  interval={INTERVAL}s  |  max_flows={MAX_FLOWS or 'unlimited'}")

    flows_processed = 0
    pass_number = 0

    while not _stop:
        pass_number += 1
        log.info(f"--- Pass {pass_number}: shuffling {total_rows} rows ---")

        shuffled = features_df.sample(frac=1).reset_index(drop=True)

        for _, row in shuffled.iterrows():
            if _stop:
                break
            if MAX_FLOWS and flows_processed >= MAX_FLOWS:
                _stop = True
                break

            row_dict = row.to_dict()

            db = SessionLocal()
            try:
                alert = _process_flow(row_dict, db)
            except Exception as exc:
                log.error(f"Flow processing error: {exc}")
                continue
            finally:
                db.close()

            flows_processed += 1
            log.info(
                f"[{flows_processed}] alert_id={alert['alert_id']}  "
                f"prediction={alert['prediction']}  "
                f"severity={alert['severity']}  "
                f"risk={alert['risk_score']}"
            )

            if not _stop:
                time.sleep(INTERVAL)

    log.info(f"Simulator stopped. Total flows processed: {flows_processed}")


if __name__ == "__main__":
    run()
