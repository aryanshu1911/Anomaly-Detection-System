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