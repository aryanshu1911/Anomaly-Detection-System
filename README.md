# SentinelAI

## Overview

SentinelAI is an AI-powered cybersecurity platform designed to detect malicious network activity and identify anomalous behavior within enterprise network traffic.

The project combines machine learning, anomaly detection, threat analysis, and security operations workflows to simulate a modern Security Operations Center (SOC) detection platform.

---

## Objectives

* Detect malicious network activity
* Identify anomalous behavior
* Reduce false positives
* Prioritize security alerts
* Support incident investigation
* Provide explainable detection results
* Deliver a production-style security dashboard

---

## Dataset

Dataset Used: UNSW-NB15

Training Set:

* 175,341 records
* 36 features

Testing Set:

* 82,332 records
* 36 features

Target Variables:

* label (Normal vs Attack)
* attack_cat (Attack Category)

---

## Project Workflow

Network Traffic
→ Data Exploration
→ Feature Analysis
→ Correlation Analysis
→ Baseline Detection Models
→ Anomaly Detection Engine
→ Risk Scoring
→ Alert Generation
→ Investigation Workflow
→ SOC Dashboard

---

## Phase 1: Security Data Analysis

Completed:

* Dataset profiling
* Attack distribution analysis
* Feature correlation analysis
* Threat behavior investigation

Key Findings:

Important attack indicators:

* dload
* rate
* sload
* tcprtt
* synack
* ackdat
* ct_dst_sport_ltm
* ct_src_dport_ltm

---

## Phase 2: Baseline Detection Models

### Logistic Regression

Accuracy: 60.57%

Precision: 58.27%

Recall: 99.99%

F1 Score: 73.63%

Observation:

The model achieved near-perfect recall but produced excessive false positives, making it unsuitable for operational deployment.

---

### Random Forest

Accuracy: 86.78%

Precision: 82.15%

Recall: 97.07%

F1 Score: 88.99%

Observation:

Random Forest significantly reduced false positives while maintaining strong attack detection performance.

---

## Feature Importance

Top Features:

1. dload
2. ackdat
3. rate
4. synack
5. tcprtt
6. sload
7. dmean
8. sbytes
9. dur
10. sinpkt

---

## Upcoming Milestones

### Phase 3

Isolation Forest

Goal:

Train on normal traffic only and detect anomalous behavior in unseen traffic.

---

### Phase 4

XGBoost

Goal:

Benchmark against Random Forest and improve detection performance.

---

### Phase 5

SHAP Explainability

Goal:

Explain why a network event was classified as malicious.

---

### Phase 6

Risk Scoring Engine

Goal:

Assign dynamic risk scores to detected events.

---

### Phase 7

Backend Development

Stack:

* FastAPI
* PostgreSQL

Endpoints:

* /predict
* /anomaly
* /alerts
* /cases
* /metrics

---

### Phase 8

SOC Dashboard

Features:

* Alert Monitoring
* Risk Trends
* Incident Queue
* Threat Analytics
* Investigation Workspace

---

### Phase 9

Deployment

Stack:

* Docker
* GitHub
* Cloud Deployment

---

## Current Status

Phase 1: Complete
Phase 2: Complete
Phase 3: In Progress

Current Focus:
Building Isolation Forest-based anomaly detection engine.
