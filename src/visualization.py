"""
Visualization module for the Spotify Trends Analysis project.

Responsibility:
    Generates and saves all professional-grade plots to the images/
    directory. Every plot includes:
    - Informative title
    - Labelled axes
    - Grid where appropriate
    - High DPI (300)
    - Proper layout (tight_layout)

Why this file exists:
    - Decouples plotting from analysis logic.
    - Centralizes figure settings (style, DPI, palette).
    - Makes it easy to swap backends or adjust aesthetics.
    - Each visualisation is a single callable function.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import (
    COLOR_CATEGORICAL,
    COLOR_SECONDARY,
    COLOR_TERTIARY,
    FIGURE_DPI,
    FIGURE_SIZE,
    IMAGES_DIR,
    PALETTE,
    PLOT_STYLE,
    setup_logging,
)

logger = setup_logging(__name__)


class Visualizer:
    """Generates and saves all project visualisations."""

    def __init__(
        self,
        output_dir: Path = IMAGES_DIR,
        style: str = PLOT_STYLE,
        palette: str = PALETTE,
        dpi: int = FIGURE_DPI,
    ):
        """Initialise the visualizer with plotting style preferences.

        Args:
            output_dir: Directory to save plot images.
            style: Matplotlib style string.
            palette: Seaborn colour palette.
            dpi: Figure DPI for high-resolution output.
        """
        self.output_dir = output_dir
        self.dpi = dpi
        sns.set_style(style)
        sns.set_palette(palette)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Visualizer initialised — saving to %s", output_dir)

    def _save_fig(self, filename: str) -> None:
        """Save the current matplotlib figure to disk.

        Args:
            filename: Output filename (will be saved in output_dir).
        """
        filepath = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.dpi, bbox_inches="tight")
        plt.close()
        logger.info("Saved figure: %s", filepath)

    def _configure_axes(
        self,
        ax: plt.Axes,
        title: str,
        xlabel: str,
        ylabel: str,
        grid: bool = True,
    ) -> None:
        """Apply standard axis configuration.

        Args:
            ax: Matplotlib Axes object.
            title: Plot title.
            xlabel: X-axis label.
            ylabel: Y-axis label.
            grid: Whether to show grid.
        """
        ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        if grid:
            ax.grid(True, alpha=0.3, linestyle="--")

    # ──────────────────────────────────────────────
    # Distribution plots
    # ──────────────────────────────────────────────

    def plot_popularity_distribution(
        self, popularity: pd.Series
    ) -> None:
        """Histogram of song popularity scores.

        Args:
            popularity: Series of popularity values.
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.histplot(popularity, bins=30, kde=True, color=COLOR_CATEGORICAL, ax=ax)
        self._configure_axes(
            ax,
            title="Distribution of Song Popularity",
            xlabel="Popularity Score",
            ylabel="Frequency",
        )
        self._save_fig("popularity_distribution.png")

    def plot_tempo_distribution(self, tempo: pd.Series) -> None:
        """Histogram of track tempo (BPM).

        Args:
            tempo: Series of tempo values.
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.histplot(tempo, bins=30, kde=True, color=COLOR_SECONDARY, ax=ax)
        self._configure_axes(
            ax,
            title="Distribution of Tempo (BPM)",
            xlabel="Tempo (BPM)",
            ylabel="Frequency",
        )
        self._save_fig("tempo_distribution.png")

    def plot_duration_distribution(self, duration_min: pd.Series) -> None:
        """Histogram of track duration in minutes.

        Args:
            duration_min: Series of duration in minutes.
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.histplot(
            duration_min, bins=30, kde=True, color=COLOR_TERTIARY, ax=ax
        )
        self._configure_axes(
            ax,
            title="Distribution of Track Duration",
            xlabel="Duration (minutes)",
            ylabel="Frequency",
        )
        self._save_fig("duration_distribution.png")

    # ──────────────────────────────────────────────
    # Bar charts
    # ──────────────────────────────────────────────

    def plot_top_artists(
        self, top_artists: pd.DataFrame, top_n: int = 10
    ) -> None:
        """Horizontal bar chart of top artists by track count.

        Args:
            top_artists: DataFrame with artist_name and track_count.
            top_n: Number of artists to display.
        """
        if top_artists.empty:
            logger.warning("No artist data to plot")
            return
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.barplot(
            data=top_artists.head(top_n),
            y="artist_name",
            x="track_count",
            hue="artist_name",
            palette=PALETTE,
            legend=False,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title=f"Top {top_n} Artists by Track Count",
            xlabel="Track Count",
            ylabel="Artist",
        )
        self._save_fig("top_artists.png")

    def plot_genre_distribution(
        self, genre_counts: pd.Series, top_n: int = 15
    ) -> None:
        """Horizontal bar chart of genre distribution.

        Args:
            genre_counts: Series with genre as index, count as values.
            top_n: Number of genres to display.
        """
        if genre_counts.empty:
            logger.warning("No genre data to plot")
            return
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        top_genres = genre_counts.head(top_n)
        genre_df = top_genres.reset_index()
        genre_df.columns = ["genre", "count"]
        sns.barplot(
            data=genre_df,
            x="count",
            y="genre",
            hue="genre",
            palette=PALETTE,
            legend=False,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title=f"Top {top_n} Genres by Track Count",
            xlabel="Track Count",
            ylabel="Genre",
        )
        self._save_fig("genre_distribution.png")

    def plot_most_popular_songs(
        self, popular_songs: pd.DataFrame, top_n: int = 10
    ) -> None:
        """Horizontal bar chart of most popular songs.

        Args:
            popular_songs: DataFrame with track_name, artist_name, popularity.
            top_n: Number of songs to display.
        """
        if popular_songs.empty:
            logger.warning("No popular song data to plot")
            return
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.barplot(
            data=popular_songs.head(top_n),
            y="track_name",
            x="popularity",
            hue="track_name",
            palette=PALETTE,
            legend=False,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title=f"Top {top_n} Most Popular Songs",
            xlabel="Popularity Score",
            ylabel="Track Name",
        )
        self._save_fig("most_popular_songs.png")

    def plot_average_popularity_by_genre(
        self, avg_popularity: pd.DataFrame, top_n: int = 15
    ) -> None:
        """Bar chart of average popularity by genre.

        Args:
            avg_popularity: DataFrame with genre and mean_popularity.
            top_n: Number of genres to display.
        """
        if avg_popularity.empty:
            logger.warning("No genre popularity data to plot")
            return
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        top_data = avg_popularity.head(top_n)
        sns.barplot(
            data=top_data,
            y="genre",
            x="mean_popularity",
            hue="genre",
            palette=PALETTE,
            legend=False,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title=f"Average Popularity by Genre (Top {top_n})",
            xlabel="Average Popularity",
            ylabel="Genre",
        )
        self._save_fig("average_popularity_by_genre.png")

    # ──────────────────────────────────────────────
    # Scatter plots
    # ──────────────────────────────────────────────

    def plot_danceability_vs_popularity(
        self, data: pd.DataFrame
    ) -> None:
        """Scatter plot of danceability vs popularity.

        Args:
            data: DataFrame with danceability and popularity columns.
        """
        if data.empty:
            logger.warning("No danceability vs popularity data")
            return
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.scatterplot(
            data=data,
            x="danceability",
            y="popularity",
            alpha=0.6,
            color=COLOR_CATEGORICAL,
            ax=ax,
        )
        sns.regplot(
            data=data,
            x="danceability",
            y="popularity",
            scatter=False,
            color=COLOR_SECONDARY,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title="Danceability vs Popularity",
            xlabel="Danceability",
            ylabel="Popularity",
        )
        self._save_fig("danceability_vs_popularity.png")

    def plot_energy_vs_popularity(self, data: pd.DataFrame) -> None:
        """Scatter plot of energy vs popularity with regression line.

        Args:
            data: DataFrame with energy and popularity columns.
        """
        if data.empty:
            logger.warning("No energy vs popularity data")
            return
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.scatterplot(
            data=data,
            x="energy",
            y="popularity",
            alpha=0.6,
            color=COLOR_CATEGORICAL,
            ax=ax,
        )
        sns.regplot(
            data=data,
            x="energy",
            y="popularity",
            scatter=False,
            color=COLOR_SECONDARY,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title="Energy vs Popularity",
            xlabel="Energy",
            ylabel="Popularity",
        )
        self._save_fig("energy_vs_popularity.png")

    # ──────────────────────────────────────────────
    # Box plots
    # ──────────────────────────────────────────────

    def plot_audio_feature_boxplot(
        self, df: pd.DataFrame, features: Optional[List[str]] = None
    ) -> None:
        """Box plot of audio features to show distributions and outliers.

        Args:
            df: DataFrame with audio feature columns.
            features: Specific features to include. If None, uses defaults.
        """
        if features is None:
            features = [
                "danceability",
                "energy",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "liveness",
                "valence",
            ]
        available = [c for c in features if c in df.columns]
        if not available:
            logger.warning("No audio features available for boxplot")
            return

        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.boxplot(data=df[available], palette=PALETTE, ax=ax)
        self._configure_axes(
            ax,
            title="Distribution of Audio Features",
            xlabel="Audio Feature",
            ylabel="Value",
        )
        plt.xticks(rotation=45, ha="right")
        self._save_fig("audio_feature_boxplot.png")

    # ──────────────────────────────────────────────
    # Heatmap
    # ──────────────────────────────────────────────

    def plot_correlation_heatmap(
        self, corr_matrix: pd.DataFrame
    ) -> None:
        """Heatmap of the correlation matrix.

        Args:
            corr_matrix: Correlation matrix DataFrame.
        """
        if corr_matrix.empty:
            logger.warning("No correlation matrix to plot")
            return
        fig, ax = plt.subplots(figsize=(14, 10))
        mask = None
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            linewidths=0.5,
            mask=mask,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title="Correlation Matrix of Audio Features",
            xlabel="Features",
            ylabel="Features",
            grid=False,
        )
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        self._save_fig("correlation_heatmap.png")

    # ──────────────────────────────────────────────
    # Pie chart
    # ──────────────────────────────────────────────

    def plot_genre_pie(self, genre_counts: pd.Series, top_n: int = 8) -> None:
        """Pie chart of genre distribution (top genres + 'Other').

        Only plotted if the number of genres makes it meaningful (>2).

        Args:
            genre_counts: Series with genre counts.
            top_n: Number of top genres to include before 'Other'.
        """
        if genre_counts.empty or len(genre_counts) < 3:
            logger.warning("Not enough genres for a meaningful pie chart")
            return

        top = genre_counts.head(top_n)
        other = genre_counts.iloc[top_n:].sum()
        if other > 0:
            top = pd.concat([top, pd.Series({"Other": other})])

        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(
            top.values,
            labels=top.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=sns.color_palette(PALETTE, len(top)),
            wedgeprops={"linewidth": 1, "edgecolor": "white"},
        )
        ax.set_title("Genre Distribution (Pie Chart)", fontsize=14, fontweight="bold")
        self._save_fig("genre_pie.png")

    # ──────────────────────────────────────────────
    # Line plot
    # ──────────────────────────────────────────────

    def plot_popularity_by_year(self, data: pd.DataFrame) -> None:
        """Line plot of average popularity over release years.

        Only plotted if release_year column exists.

        Args:
            data: DataFrame with release_year and mean_popularity.
        """
        if data.empty:
            logger.warning("No year-over-year popularity data")
            return
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        sns.lineplot(
            data=data,
            x="release_year",
            y="mean_popularity",
            marker="o",
            color=COLOR_CATEGORICAL,
            ax=ax,
        )
        self._configure_axes(
            ax,
            title="Average Popularity Over Time",
            xlabel="Release Year",
            ylabel="Average Popularity",
        )
        self._save_fig("popularity_by_year.png")
