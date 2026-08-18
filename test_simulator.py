"""
test_simulator.py
-----------------
Integration tests for the UNSW-NB15 replay simulator pipeline.

These tests do NOT require the FastAPI server to be running.
They exercise the core pipeline directly:

    UNSW-NB15 row → predict_network_flow() → save_alert() → DB

and verify that:
  1. predict_network_flow() returns a correctly-structured alert dict.
  2. save_alert() persists the alert to the database.
  3. The persisted alert is retrievable via get_alert().
  4. Multiple flows from a realistic mixed stream (normal + attack) all persist.
"""

import sys
import os

# Ensure the project root is on the path (needed when pytest is run from root).
_PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import pytest
import pandas as pd

from src.data_loader import load_test_data
from src.constants import DROP_COLUMNS

from backend.services.prediction_service import predict_network_flow
from backend.services.alert_service import save_alert, get_alert, get_alerts
from backend.database.connection import SessionLocal, Base, engine

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def db():
    """Provide a real SQLAlchemy session against the project database."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def sample_rows():
    """
    Load 10 rows from the UNSW-NB15 test dataset, stripping target columns.
    These represent a realistic mixed telemetry stream (normal + attack flows).
    """
    df = load_test_data()
    drop = [c for c in DROP_COLUMNS if c in df.columns]
    features_df = df.drop(columns=drop)
    # Take a deterministic sample for reproducibility
    return features_df.head(10)


@pytest.fixture(scope="module")
def single_row(sample_rows):
    """Return the first row as a dict — the format predict_network_flow expects."""
    return sample_rows.iloc[0].to_dict()


# ---------------------------------------------------------------------------
# Unit-level: predict_network_flow output structure
# ---------------------------------------------------------------------------

class TestPredictNetworkFlow:

    def test_returns_dict(self, single_row):
        alert = predict_network_flow(single_row)
        assert isinstance(alert, dict)

    def test_alert_id_format(self, single_row):
        alert = predict_network_flow(single_row)
        assert "alert_id" in alert
        assert alert["alert_id"].startswith("ALT-")
        assert len(alert["alert_id"]) == 12  # "ALT-" + 8 hex chars

    def test_required_fields_present(self, single_row):
        alert = predict_network_flow(single_row)
        required = {
            "alert_id", "timestamp", "status",
            "prediction", "probability", "risk_score",
            "severity", "priority", "recommendation",
        }
        assert required.issubset(alert.keys())

    def test_prediction_is_valid(self, single_row):
        alert = predict_network_flow(single_row)
        assert alert["prediction"] in ("Attack", "Normal")

    def test_probability_in_range(self, single_row):
        alert = predict_network_flow(single_row)
        assert 0.0 <= alert["probability"] <= 1.0

    def test_risk_score_in_range(self, single_row):
        alert = predict_network_flow(single_row)
        assert 0 <= alert["risk_score"] <= 100

    def test_severity_is_valid(self, single_row):
        alert = predict_network_flow(single_row)
        assert alert["severity"] in ("Low", "Medium", "High", "Critical")

    def test_priority_is_valid(self, single_row):
        alert = predict_network_flow(single_row)
        assert alert["priority"] in ("P1", "P2", "P3", "P4")

    def test_status_is_open(self, single_row):
        alert = predict_network_flow(single_row)
        assert alert["status"] == "Open"


# ---------------------------------------------------------------------------
# Persistence: save_alert → get_alert
# ---------------------------------------------------------------------------

class TestPersistence:

    def test_save_and_retrieve_alert(self, db, single_row):
        alert_dict = predict_network_flow(single_row)
        saved = save_alert(db, alert_dict)

        assert saved is not None
        assert saved.id == alert_dict["alert_id"]

        retrieved = get_alert(db, alert_dict["alert_id"])
        assert retrieved is not None
        assert retrieved.id == alert_dict["alert_id"]
        assert retrieved.prediction == alert_dict["prediction"]
        assert retrieved.severity == alert_dict["severity"]
        assert retrieved.priority == alert_dict["priority"]
        assert retrieved.status == "Open"

    def test_multiple_flows_persist(self, db, sample_rows):
        """
        Process 5 rows from the mixed stream (normal + attack) and verify
        all are persisted to the database.
        """
        drop = [c for c in DROP_COLUMNS if c in sample_rows.columns]
        rows_subset = sample_rows.drop(columns=drop, errors="ignore").head(5)

        alert_ids = []
        for _, row in rows_subset.iterrows():
            alert_dict = predict_network_flow(row.to_dict())
            save_alert(db, alert_dict)
            alert_ids.append(alert_dict["alert_id"])

        # All 5 alerts must be independently retrievable
        for aid in alert_ids:
            fetched = get_alert(db, aid)
            assert fetched is not None, f"Alert {aid} not found in DB"

    def test_get_alerts_returns_list(self, db):
        alerts = get_alerts(db)
        assert isinstance(alerts, list)
        assert len(alerts) >= 1  # at least what we just inserted


# ---------------------------------------------------------------------------
# Single-persistence-path assertion
# ---------------------------------------------------------------------------

class TestSinglePersistencePath:
    """
    Verifies that the simulator pipeline uses exactly one path into the DB:
        predict_network_flow() → save_alert()
    No duplicate alert-generation logic is exercised.
    """

    def test_predict_network_flow_does_not_auto_persist(self, single_row):
        """
        Calling predict_network_flow() alone must NOT write to the DB.
        Only save_alert() should persist.
        """
        alert_dict = predict_network_flow(single_row)
        alert_id = alert_dict["alert_id"]

        # Fresh session to avoid any session-level caching
        fresh_db = SessionLocal()
        try:
            result = get_alert(fresh_db, alert_id)
            # predict_network_flow alone should not have persisted anything
            assert result is None, (
                "predict_network_flow() persisted an alert on its own — "
                "single-persistence-path contract violated."
            )
        finally:
            fresh_db.close()
