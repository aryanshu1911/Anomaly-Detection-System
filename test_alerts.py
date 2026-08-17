import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="module")
def alerts():
    response = requests.get(f"{BASE_URL}/alerts")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    return data


@pytest.fixture(scope="module")
def valid_alert_id(alerts):
    assert alerts, "No alerts available in database for testing"
    return alerts[0]["id"]


def test_get_alerts():
    response = requests.get(f"{BASE_URL}/alerts")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_get_alerts_pagination():
    response = requests.get(
        f"{BASE_URL}/alerts?limit=2&offset=1"
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2


def test_get_alerts_filtered(alerts):
    first = alerts[0]

    response = requests.get(
        f"{BASE_URL}/alerts?severity={first['severity']}"
    )

    assert response.status_code == 200
    assert all(
        alert["severity"] == first["severity"]
        for alert in response.json()
    )

    response = requests.get(
        f"{BASE_URL}/alerts?priority={first['priority']}"
    )

    assert response.status_code == 200
    assert all(
        alert["priority"] == first["priority"]
        for alert in response.json()
    )

    response = requests.get(
        f"{BASE_URL}/alerts?status={first['status']}"
    )

    assert response.status_code == 200
    assert all(
        alert["status"] == first["status"]
        for alert in response.json()
    )

    response = requests.get(
        f"{BASE_URL}/alerts?prediction={first['prediction']}"
    )

    assert response.status_code == 200
    assert all(
        alert["prediction"] == first["prediction"]
        for alert in response.json()
    )


def test_get_single_alert(valid_alert_id):
    response = requests.get(
        f"{BASE_URL}/alerts/{valid_alert_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == valid_alert_id


def test_get_invalid_alert():
    response = requests.get(
        f"{BASE_URL}/alerts/invalid-id-xyz"
    )

    assert response.status_code == 404


def test_patch_alert(valid_alert_id):
    response = requests.patch(
        f"{BASE_URL}/alerts/{valid_alert_id}",
        json={"status": "Investigating"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Investigating"


def test_patch_invalid_alert():
    response = requests.patch(
        f"{BASE_URL}/alerts/invalid-id-xyz",
        json={"status": "Investigating"},
    )

    assert response.status_code == 404


def test_patch_invalid_status(valid_alert_id):
    response = requests.patch(
        f"{BASE_URL}/alerts/{valid_alert_id}",
        json={"status": "InvalidStatus"},
    )

    assert response.status_code == 422


def test_post_predict():
    payload = {
        "dur": 0.12,
        "proto": "tcp",
        "service": "http",
        "state": "FIN",
        "spkts": 10,
        "dpkts": 8,
        "sbytes": 500,
        "dbytes": 300,
        "rate": 50.0,
        "sload": 20.0,
        "dload": 15.0,
        "sloss": 0,
        "dloss": 0,
        "sinpkt": 1.0,
        "dinpkt": 1.0,
        "sjit": 0.1,
        "djit": 0.1,
        "swin": 255,
        "stcpb": 100,
        "dtcpb": 100,
        "dwin": 255,
        "tcprtt": 0.05,
        "synack": 0.02,
        "ackdat": 0.03,
        "smean": 50,
        "dmean": 40,
        "trans_depth": 1,
        "response_body_len": 100,
        "ct_src_dport_ltm": 1,
        "ct_dst_sport_ltm": 1,
        "is_ftp_login": 0,
        "ct_ftp_cmd": 0,
        "ct_flw_http_mthd": 1,
        "is_sm_ips_ports": 0,
    }

    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
    )

    assert response.status_code == 200

    alert_id = response.json()["alert_id"]
    assert alert_id

    # Verify persistence
    persisted = requests.get(
        f"{BASE_URL}/alerts/{alert_id}"
    )

    assert persisted.status_code == 200
    assert persisted.json()["id"] == alert_id