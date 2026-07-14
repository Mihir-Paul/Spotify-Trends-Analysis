"""
Configuration module for the Spotify Trends Analysis project.

Centralizes all paths, constants, logging settings, and visualization
parameters in one place. This follows the Separation of Concerns
principle — configuration is isolated from business logic.

Why this file exists:
    - Avoids hard-coded strings scattered across modules.
    - Makes the pipeline easy to reconfigure (e.g., change DPI, figure size).
    - Centralizes logging setup for consistent behaviour.
    - Follows the DRY principle by defining constants once.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple

# ──────────────────────────────────────────────
# Project paths
# ──────────────────────────────────────────────
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
IMAGES_DIR: Path = PROJECT_ROOT / "images"
NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"

# ──────────────────────────────────────────────
# Data paths
# ──────────────────────────────────────────────
RAW_DATA_PATH: Path = DATA_DIR / "spotify.csv"

# ──────────────────────────────────────────────
# Column definitions
# ──────────────────────────────────────────────
NUMERIC_FEATURES: List[str] = [
    "popularity",
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "loudness",
]

CATEGORICAL_FEATURES: List[str] = [
    "genre",
    "artist_name",
    "album_name",
    "track_name",
]

TARGET_FEATURE: str = "popularity"

COLUMNS_TO_DROP: List[str] = [
    "album_name",
]

# ──────────────────────────────────────────────
# Cleaning parameters
# ──────────────────────────────────────────────
MAX_DUPLICATE_SUBSET: List[str] = [
    "track_name",
    "artist_name",
]

DURATION_MINUTES_COL: str = "duration_min"

# ──────────────────────────────────────────────
# Visualisation settings
# ──────────────────────────────────────────────
FIGURE_SIZE: Tuple[int, int] = (12, 7)
FIGURE_DPI: int = 300
PALETTE: str = "viridis"
COLOR_CATEGORICAL: str = "#1DB954"  # Spotify green
COLOR_SECONDARY: str = "#191414"  # Spotify black
COLOR_TERTIARY: str = "#FF6B6B"

PLOT_STYLE: str = "whitegrid"

# ──────────────────────────────────────────────
# Logging configuration
# ──────────────────────────────────────────────
LOG_LEVEL: int = logging.INFO
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def setup_logging(name: str = __name__) -> logging.Logger:
    """Configure and return a logger with the standard format.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        )
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
        logger.propagate = False
    return logger


# ──────────────────────────────────────────────
# Analysis thresholds
# ──────────────────────────────────────────────
TOP_N_ARTISTS: int = 10
TOP_N_SONGS: int = 10
POPULARITY_THRESHOLD: int = 70  # Songs above this are "high popularity"
LOW_POPULARITY_THRESHOLD: int = 30

# ──────────────────────────────────────────────
# Kaggle dataset configuration
# ──────────────────────────────────────────────
KAGGLE_DATASET_SLUG: str = "maharshipandya/-spotify-tracks-dataset"
KAGGLE_DATASET_FILENAME: str = "dataset.csv"

# ──────────────────────────────────────────────
# Rename mapping
# ──────────────────────────────────────────────
COLUMN_RENAME_MAP: Dict[str, str] = {
    "duration_ms": DURATION_MINUTES_COL,
}

# ──────────────────────────────────────────────
# Kaggle column mapping (Kaggle -> Project)
# ──────────────────────────────────────────────
KAGGLE_COLUMN_MAP: Dict[str, str] = {
    "artists": "artist_name",
    "track_genre": "genre",
}
