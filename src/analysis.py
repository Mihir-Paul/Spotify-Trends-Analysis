"""
Exploratory Data Analysis module for the Spotify Trends Analysis project.

Responsibility:
    Computes all analytical summaries and statistical insights:
    - Top artists and songs
    - Genre distribution
    - Popularity distribution
    - Correlation analysis
    - Audio feature summaries
    - Temporal trends

Why this file exists:
    - Separates analytical logic from cleaning and visualisation.
    - Each analysis is a self-contained, reusable function.
    - Follows Single Responsibility — easy to test and extend.
"""

from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from src.config import (
    TOP_N_ARTISTS,
    TOP_N_SONGS,
    setup_logging,
)
from src.utils import time_it

logger = setup_logging(__name__)


class Analyzer:
    """Encapsulates all analytical operations on the cleaned dataset."""

    def __init__(self, df: pd.DataFrame):
        """Initialise the analyzer with a cleaned DataFrame.

        Args:
            df: Cleaned DataFrame.
        """
        self.df = df.copy()

    @time_it
    def top_artists(self, n: int = TOP_N_ARTISTS) -> pd.DataFrame:
        """Return the top N most frequent artists by track count.

        Args:
            n: Number of top artists to return.

        Returns:
            DataFrame with artist_name and track_count.
        """
        if "artist_name" not in self.df.columns:
            logger.warning("Column 'artist_name' not found")
            return pd.DataFrame()

        top = (
            self.df["artist_name"]
            .value_counts()
            .head(n)
            .reset_index()
        )
        top.columns = ["artist_name", "track_count"]
        logger.info("Top %d artists computed", n)
        return top

    @time_it
    def most_popular_songs(self, n: int = TOP_N_SONGS) -> pd.DataFrame:
        """Return the N most popular songs by popularity score.

        Args:
            n: Number of songs to return.

        Returns:
            DataFrame with track, artist, and popularity.
        """
        required = {"track_name", "artist_name", "popularity"}
        missing = required - set(self.df.columns)
        if missing:
            logger.warning("Missing columns for popular songs: %s", missing)
            return pd.DataFrame()

        top = (
            self.df[["track_name", "artist_name", "popularity"]]
            .dropna()
            .sort_values("popularity", ascending=False)
            .head(n)
            .reset_index(drop=True)
        )
        logger.info("Top %d most popular songs computed", n)
        return top

    @time_it
    def genre_distribution(self) -> pd.Series:
        """Return the count of tracks per genre.

        Returns:
            Series with genre counts (sorted descending).
        """
        if "genre" not in self.df.columns:
            logger.warning("Column 'genre' not found")
            return pd.Series(dtype=int)

        return self.df["genre"].value_counts()

    @time_it
    def popularity_distribution(self) -> pd.Series:
        """Return the popularity column values.

        Returns:
            Series of popularity values.
        """
        if "popularity" not in self.df.columns:
            logger.warning("Column 'popularity' not found")
            return pd.Series(dtype=float)

        return self.df["popularity"]

    @time_it
    def average_popularity_by_genre(self) -> pd.DataFrame:
        """Compute average popularity per genre.

        Returns:
            DataFrame with genre and mean_popularity (sorted descending).
        """
        if {"genre", "popularity"}.issubset(self.df.columns):
            return (
                self.df.groupby("genre", observed=True)["popularity"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
                .rename(columns={"popularity": "mean_popularity"})
            )
        logger.warning("Columns 'genre'/'popularity' not found")
        return pd.DataFrame()

    @time_it
    def correlation_matrix(self) -> pd.DataFrame:
        """Compute the correlation matrix of all numeric features.

        Returns:
            Correlation matrix as a DataFrame.
        """
        numeric_df = self.df.select_dtypes(include=["number"])
        if numeric_df.empty:
            logger.warning("No numeric columns available for correlation")
            return pd.DataFrame()
        return numeric_df.corr()

    @time_it
    def audio_feature_summary(self) -> pd.DataFrame:
        """Return descriptive statistics for key audio features.

        Returns:
            DataFrame with mean, median, std, min, max for each feature.
        """
        audio_features = [
            "danceability",
            "energy",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "loudness",
            "duration_min",
        ]
        available = [c for c in audio_features if c in self.df.columns]
        if not available:
            logger.warning("No audio features available for summary")
            return pd.DataFrame()
        return self.df[available].describe().T

    @time_it
    def average_duration(self) -> Dict[str, float]:
        """Return average track duration in minutes.

        Returns:
            Dictionary with mean, median, std of duration.
        """
        if "duration_min" not in self.df.columns:
            if "duration_ms" in self.df.columns:
                duration = self.df["duration_ms"] / 60_000.0
            else:
                logger.warning("No duration column available")
                return {}
        else:
            duration = self.df["duration_min"]

        return {
            "mean_min": float(round(duration.mean(), 2)),
            "median_min": float(round(duration.median(), 2)),
            "std_min": float(round(duration.std(), 2)),
        }

    @time_it
    def popularity_by_year(self) -> pd.DataFrame:
        """Compute average popularity per release year (if column exists).

        Returns:
            DataFrame with release_year and mean_popularity.
        """
        if "release_year" not in self.df.columns:
            logger.warning("Column 'release_year' not found")
            return pd.DataFrame()

        return (
            self.df.groupby("release_year", observed=True)["popularity"]
            .mean()
            .reset_index()
            .rename(columns={"popularity": "mean_popularity"})
        )

    @time_it
    def danceability_vs_popularity(self) -> pd.DataFrame:
        """Return danceability and popularity columns for scatter analysis.

        Returns:
            DataFrame with danceability and popularity.
        """
        if {"danceability", "popularity"}.issubset(self.df.columns):
            return self.df[["danceability", "popularity"]].dropna()
        logger.warning("Columns for danceability vs popularity not found")
        return pd.DataFrame()

    @time_it
    def energy_vs_popularity(self) -> pd.DataFrame:
        """Return energy and popularity columns for scatter analysis.

        Returns:
            DataFrame with energy and popularity.
        """
        if {"energy", "popularity"}.issubset(self.df.columns):
            return self.df[["energy", "popularity"]].dropna()
        logger.warning("Columns for energy vs popularity not found")
        return pd.DataFrame()

    @time_it
    def grouped_stats(
        self, group_col: str, agg_col: str, agg_func: str = "mean"
    ) -> pd.DataFrame:
        """Generic grouped aggregation helper.

        Args:
            group_col: Column to group by.
            agg_col: Column to aggregate.
            agg_func: Aggregation function (mean, median, sum, etc.).

        Returns:
            DataFrame with grouped and aggregated values.
        """
        if {group_col, agg_col}.issubset(self.df.columns):
            return (
                self.df.groupby(group_col, observed=True)[agg_col]
                .agg(agg_func)
                .sort_values(ascending=False)
                .reset_index()
            )
        logger.warning("Columns '%s'/'%s' not found", group_col, agg_col)
        return pd.DataFrame()
