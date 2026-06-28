# Dataset columns
TARGET_COLUMN = "label"
ATTACK_COLUMN = "attack_cat"

# Categorical features
CATEGORICAL_COLUMNS = [
    "proto",
    "service",
    "state"
]

# Columns to remove before prediction
DROP_COLUMNS = [
    TARGET_COLUMN,
    ATTACK_COLUMN
]

# Severity Levels
SEVERITY_LOW = "Low"
SEVERITY_MEDIUM = "Medium"
SEVERITY_HIGH = "High"
SEVERITY_CRITICAL = "Critical"

# Alert Priorities
PRIORITY_P1 = "P1"
PRIORITY_P2 = "P2"
PRIORITY_P3 = "P3"
PRIORITY_P4 = "P4"

# Risk Score Thresholds
LOW_THRESHOLD = 25
MEDIUM_THRESHOLD = 50
HIGH_THRESHOLD = 75

# Alert Status
STATUS_OPEN = "Open"
STATUS_INVESTIGATING = "Investigating"
STATUS_RESOLVED = "Resolved"
STATUS_CLOSED = "Closed"

# Alert Prefix
ALERT_PREFIX = "ALT"