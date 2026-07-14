"""
Utility / helper module for the Spotify Trends Analysis project.

Responsibility:
    Provides reusable utility functions used across the pipeline:
    - Timing/decorator utilities
    - Data validation helpers
    - Common file I/O operations
    - Unit conversion helpers

Why this file exists:
    - Keeps helper functions out of business-logic modules.
    - Promotes reuse and testability.
    - Follows the Single Responsibility Principle.
"""

import time
import functools
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

from src.config import (
    KAGGLE_COLUMN_MAP,
    KAGGLE_DATASET_FILENAME,
    KAGGLE_DATASET_SLUG,
    setup_logging,
)

logger = setup_logging(__name__)


# ──────────────────────────────────────────────
# Timing decorator
# ──────────────────────────────────────────────
def time_it(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that logs the execution duration of a function.

    Useful for profiling pipeline stages and identifying bottlenecks.

    Args:
        func: The function to wrap.

    Returns:
        Wrapped function with timing logic.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("%s executed in %.4f seconds", func.__name__, elapsed)
        return result

    return wrapper


# ──────────────────────────────────────────────
# Data validation helpers
# ──────────────────────────────────────────────
def validate_columns(
    df: pd.DataFrame,
    required: Optional[List[str]] = None,
    optional: Optional[List[str]] = None,
) -> List[str]:
    """Check which required columns are missing from the DataFrame.

    Gracefully handles missing columns — logs warnings but does not crash.

    Args:
        df: Input DataFrame.
        required: Columns that must be present.
        optional: Columns that are nice-to-have.

    Returns:
        List of missing required columns (empty if all present).
    """
    required = required or []
    optional = optional or []
    all_cols = set(df.columns)
    missing_required = [c for c in required if c not in all_cols]
    missing_optional = [c for c in optional if c not in all_cols]

    if missing_required:
        logger.warning("Missing required columns: %s", missing_required)
    if missing_optional:
        logger.info("Missing optional columns: %s", missing_optional)

    return missing_required


def safe_convert_numeric(
    df: pd.DataFrame,
    column: str,
    fallback: Any = None,
) -> pd.Series:
    """Safely convert a column to numeric, coercing errors.

    Args:
        df: Input DataFrame.
        column: Column name to convert.
        fallback: Value to fill after coercion NaN.

    Returns:
        Numeric Series.
    """
    result = pd.to_numeric(df[column], errors="coerce")
    n_coerced = result.isna().sum() - df[column].isna().sum()
    if n_coerced > 0:
        logger.warning(
            "Coerced %d non-numeric values in '%s' to NaN", n_coerced, column
        )
    if fallback is not None:
        result = result.fillna(fallback)
    return result


# ──────────────────────────────────────────────
# Unit conversion helpers
# ──────────────────────────────────────────────
def milliseconds_to_minutes(ms: float) -> float:
    """Convert milliseconds to minutes.

    Args:
        ms: Duration in milliseconds.

    Returns:
        Duration in minutes (rounded to 2 decimal places).
    """
    return round(ms / 60_000.0, 2)


# ──────────────────────────────────────────────
# Summary helpers
# ──────────────────────────────────────────────
def dataframe_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Return a concise summary dictionary of a DataFrame.

    Args:
        df: Input DataFrame.

    Returns:
        Dictionary with shape, columns, dtypes, missing values, duplicates.
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isna().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "total_cells": df.size,
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1_024**2, 2),
    }


# ──────────────────────────────────────────────
# Kaggle dataset loader
# ──────────────────────────────────────────────
@time_it
def load_from_kaggle() -> pd.DataFrame:
    """Load the Spotify tracks dataset directly from Kaggle.

    Downloads and caches the latest version of the dataset from:
    https://kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

    The returned DataFrame has columns renamed to match the project's
    conventions (e.g., 'artists' -> 'artist_name', 'track_genre' -> 'genre').

    Returns:
        DataFrame containing the full Kaggle dataset.

    Raises:
        ImportError: If kagglehub is not installed.
    """
    try:
        import kagglehub
        from kagglehub import KaggleDatasetAdapter
    except ImportError:
        raise ImportError(
            "kagglehub is required to load datasets from Kaggle. "
            "Install it with: pip install kagglehub[pandas-datasets]"
        )

    logger.info("Downloading dataset from Kaggle: %s", KAGGLE_DATASET_SLUG)
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        KAGGLE_DATASET_SLUG,
        KAGGLE_DATASET_FILENAME,
    )

    # Drop unnamed index column if present
    unnamed_cols = [c for c in df.columns if c.startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
        logger.info("Dropped unnamed index columns: %s", unnamed_cols)

    # Rename columns to match project conventions
    existing_renames = {
        k: v for k, v in KAGGLE_COLUMN_MAP.items() if k in df.columns
    }
    if existing_renames:
        df = df.rename(columns=existing_renames)
        logger.info("Renamed Kaggle columns: %s", existing_renames)

    logger.info(
        "Loaded Kaggle dataset — shape: %s, columns: %s",
        df.shape,
        list(df.columns),
    )
    return df
