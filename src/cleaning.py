"""
Data cleaning module for the Spotify Trends Analysis project.

Responsibility:
    Provides a complete data cleaning pipeline:
    - Removing duplicate records
    - Handling missing values (numeric and categorical)
    - Converting data types (e.g., duration_ms → duration_min)
    - Renaming columns for readability
    - Dropping irrelevant columns

Why this file exists:
    - Separates cleaning logic from analysis/visualisation concerns.
    - Makes the pipeline modular: swap or extend cleaning steps easily.
    - Follows the Single Responsibility and Open/Closed principles.
"""

from typing import Any, Dict, List, Optional

import pandas as pd

from src.config import (
    COLUMN_RENAME_MAP,
    COLUMNS_TO_DROP,
    DURATION_MINUTES_COL,
    MAX_DUPLICATE_SUBSET,
    NUMERIC_FEATURES,
    setup_logging,
)
from src.utils import milliseconds_to_minutes, safe_convert_numeric, time_it

logger = setup_logging(__name__)


class DataCleaner:
    """Encapsulates all data cleaning operations.

    Usage:
        cleaner = DataCleaner()
        df_clean = cleaner.clean(df_raw)
    """

    def __init__(
        self,
        rename_map: Optional[Dict[str, str]] = None,
        columns_to_drop: Optional[List[str]] = None,
        duplicate_subset: Optional[List[str]] = None,
    ):
        """Initialise cleaner with optional overrides for config defaults.

        Args:
            rename_map: Column rename mapping.
            columns_to_drop: Columns to drop.
            duplicate_subset: Columns to consider for duplicate detection.
        """
        self.rename_map = rename_map or COLUMN_RENAME_MAP
        self.columns_to_drop = columns_to_drop or COLUMNS_TO_DROP
        self.duplicate_subset = duplicate_subset or MAX_DUPLICATE_SUBSET

    @time_it
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Execute the full cleaning pipeline on a raw DataFrame.

        Steps:
            1. Remove duplicates
            2. Handle missing values
            3. Convert duration to minutes
            4. Rename columns
            5. Drop irrelevant columns
            6. Convert data types

        Args:
            df: Raw input DataFrame.

        Returns:
            Cleaned DataFrame.
        """
        df = df.copy()

        df = self._remove_duplicates(df)
        df = self._handle_missing_values(df)
        df = self._convert_duration(df)
        df = self._rename_columns(df)
        df = self._convert_dtypes(df)

        logger.info("Cleaning complete. Shape: %s", df.shape)
        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows based on track name and artist.

        Duplicates distort analysis — the same song appearing multiple times
        would inflate its perceived popularity.

        Args:
            df: Input DataFrame.

        Returns:
            DataFrame with duplicates removed.
        """
        before = len(df)
        df = df.drop_duplicates(subset=self.duplicate_subset, keep="first")
        removed = before - len(df)
        if removed:
            logger.info("Removed %d duplicate rows", removed)
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values gracefully.

        Strategy:
            - Numeric columns: fill with median (robust to outliers).
            - Categorical columns: fill with 'Unknown'.
            - Rows with >50% missing are dropped.

        Args:
            df: Input DataFrame.

        Returns:
            DataFrame with missing values handled.
        """
        # Drop rows with >50% missing values
        threshold = len(df.columns) / 2
        before = len(df)
        df = df.dropna(thresh=threshold)
        dropped = before - len(df)
        if dropped:
            logger.info("Dropped %d rows with excessive missing values", dropped)

        numeric_cols = df.select_dtypes(include=["number"]).columns
        categorical_cols = df.select_dtypes(include=["object"]).columns

        for col in numeric_cols:
            missing = df[col].isna().sum()
            if missing:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                logger.info("Filled %d missing values in '%s' with median %.2f", missing, col, median_val)

        for col in categorical_cols:
            missing = df[col].isna().sum()
            if missing:
                df[col] = df[col].fillna("Unknown")
                logger.info("Filled %d missing values in '%s' with 'Unknown'", missing, col)

        return df

    def _convert_duration(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert duration_ms to minutes and drop the original column.

        Minutes are more interpretable for human readers than milliseconds.
        The original milliseconds column is dropped to avoid data duplication.

        Args:
            df: Input DataFrame.

        Returns:
            DataFrame with duration in minutes (no duration_ms column).
        """
        if "duration_ms" in df.columns:
            df[DURATION_MINUTES_COL] = df["duration_ms"].apply(
                milliseconds_to_minutes
            )
            # Remove the raw milliseconds column to avoid confusion with rename
            if DURATION_MINUTES_COL in self.rename_map.values():
                df = df.drop(columns=["duration_ms"])
            logger.info("Converted duration_ms to %s", DURATION_MINUTES_COL)
        else:
            logger.warning("Column 'duration_ms' not found — skipping conversion")
        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename columns for readability.

        Args:
            df: Input DataFrame.

        Returns:
            DataFrame with renamed columns.
        """
        existing = {k: v for k, v in self.rename_map.items() if k in df.columns}
        if existing:
            df = df.rename(columns=existing)
            logger.info("Renamed columns: %s", existing)
        return df

    def _convert_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to appropriate data types.

        Ensures numeric columns are float/int and categorical columns
        are the 'category' dtype for memory efficiency.

        Args:
            df: Input DataFrame.

        Returns:
            DataFrame with optimised dtypes.
        """
        for col in df.select_dtypes(include=["object"]).columns:
            if df[col].nunique() < len(df) * 0.5:
                df[col] = df[col].astype("category")

        numeric_features_available = [
            c for c in NUMERIC_FEATURES if c in df.columns
        ]
        for col in numeric_features_available:
            if df[col].dtype == "object":
                df[col] = safe_convert_numeric(df, col, fallback=df[col].median())

        logger.info("Data types optimised")
        return df
