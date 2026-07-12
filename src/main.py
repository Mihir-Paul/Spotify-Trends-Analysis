"""
Command-line entry point for the Spotify Trends Analysis pipeline.

Usage:
    python -m src.main                    # Use default path
    python -m src.main --input path/to/data.csv
    python -m src.main --input data.csv --output-dir custom_images
    python -m src.main --skip-visualization

Why this file exists:
    - Provides a clean, runnable CLI interface.
    - Orchestrates the full pipeline: load → inspect → clean → analyze → visualize.
    - Follows the "Script" pattern with argparse for flexibility.
"""

import argparse
import sys
from pathlib import Path
from typing import NoReturn

import pandas as pd

from src.analysis import Analyzer
from src.cleaning import DataCleaner
from src.config import (
    RAW_DATA_PATH,
    IMAGES_DIR,
    setup_logging,
)
from src.utils import dataframe_summary, time_it, validate_columns
from src.visualization import Visualizer

logger = setup_logging(__name__)


# ──────────────────────────────────────────────
# Argument parser
# ──────────────────────────────────────────────
def parse_args(argv: list = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Command-line argument list (defaults to sys.argv[1:]).

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Spotify Trends Analysis — EDA Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Example:\n"
            "  python -m src.main\n"
            "  python -m src.main --input data/spotify.csv --skip-visualization\n"
        ),
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(RAW_DATA_PATH),
        help=f"Path to input CSV (default: {RAW_DATA_PATH})",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(IMAGES_DIR),
        help="Directory to save visualizations (default: images/)",
    )
    parser.add_argument(
        "--skip-visualization",
        action="store_true",
        help="Skip the visualization step",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Spotify Trends Analysis v2.0.0",
    )
    return parser.parse_args(argv)


# ──────────────────────────────────────────────
# Pipeline steps
# ──────────────────────────────────────────────
@time_it
def load_data(filepath: Path) -> pd.DataFrame:
    """Load the CSV dataset into a DataFrame.

    Args:
        filepath: Path to the CSV file.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    df = pd.read_csv(filepath)
    logger.info("Loaded dataset: %s — shape: %s", filepath, df.shape)
    return df


@time_it
def inspect_data(df: pd.DataFrame) -> None:
    """Print dataset inspection details to the log.

    Args:
        df: Input DataFrame to inspect.
    """
    summary = dataframe_summary(df)
    logger.info("Dataset shape: %s", summary["shape"])
    logger.info("Columns: %s", summary["columns"])
    logger.info("Missing values: %s", {k: v for k, v in summary["missing_values"].items() if v > 0})
    logger.info("Duplicate rows: %d", summary["duplicates"])
    logger.info("Memory usage: %.2f MB", summary["memory_usage_mb"])


@time_it
def run_pipeline(args: argparse.Namespace) -> None:
    """Execute the full EDA pipeline.

    Steps:
        1. Load data
        2. Inspect data
        3. Clean data
        4. Analyze data
        5. Visualize data

    Args:
        args: Parsed command-line arguments.
    """
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    # ── Step 1: Load ────────────────────────
    logger.info("=" * 60)
    logger.info("STEP 1: Loading dataset")
    logger.info("=" * 60)
    df = load_data(input_path)
    validate_columns(df)

    # ── Step 2: Inspect ─────────────────────
    logger.info("=" * 60)
    logger.info("STEP 2: Inspecting dataset")
    logger.info("=" * 60)
    inspect_data(df)

    # ── Step 3: Clean ───────────────────────
    logger.info("=" * 60)
    logger.info("STEP 3: Cleaning dataset")
    logger.info("=" * 60)
    cleaner = DataCleaner()
    df_clean = cleaner.clean(df)

    # ── Step 4: Analyze ─────────────────────
    logger.info("=" * 60)
    logger.info("STEP 4: Exploratory Data Analysis")
    logger.info("=" * 60)
    analyzer = Analyzer(df_clean)

    top_artists = analyzer.top_artists()
    popular_songs = analyzer.most_popular_songs()
    genre_dist = analyzer.genre_distribution()
    popularity = analyzer.popularity_distribution()
    avg_pop_by_genre = analyzer.average_popularity_by_genre()
    corr_matrix = analyzer.correlation_matrix()
    audio_summary = analyzer.audio_feature_summary()
    avg_duration = analyzer.average_duration()
    popularity_by_year = analyzer.popularity_by_year()
    dance_pop = analyzer.danceability_vs_popularity()
    energy_pop = analyzer.energy_vs_popularity()

    logger.info("Top artists:\n%s", top_artists.head(5).to_string(index=False))
    logger.info("Most popular songs:\n%s", popular_songs.head(5).to_string(index=False))
    logger.info("Average duration: %s", avg_duration)
    logger.info("Audio feature summary:\n%s", audio_summary.head().to_string())

    # ── Step 5: Visualize ──────────────────
    if not args.skip_visualization:
        logger.info("=" * 60)
        logger.info("STEP 5: Generating visualizations")
        logger.info("=" * 60)
        viz = Visualizer(output_dir=output_dir)

        viz.plot_top_artists(top_artists)
        viz.plot_genre_distribution(genre_dist)
        viz.plot_most_popular_songs(popular_songs)
        viz.plot_popularity_distribution(popularity)
        viz.plot_danceability_vs_popularity(dance_pop)
        viz.plot_energy_vs_popularity(energy_pop)
        viz.plot_tempo_distribution(df_clean["tempo"] if "tempo" in df_clean.columns else pd.Series(dtype=float))
        viz.plot_correlation_heatmap(corr_matrix)
        viz.plot_average_popularity_by_genre(avg_pop_by_genre)
        viz.plot_duration_distribution(df_clean["duration_min"] if "duration_min" in df_clean.columns else pd.Series(dtype=float))
        viz.plot_audio_feature_boxplot(df_clean)
        viz.plot_genre_pie(genre_dist)
        viz.plot_popularity_by_year(popularity_by_year)

    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 60)


def main(argv: list = None) -> None:
    """Main entry point for the CLI.

    Args:
        argv: Command-line argument list.
    """
    args = parse_args(argv)
    try:
        run_pipeline(args)
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)
    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
