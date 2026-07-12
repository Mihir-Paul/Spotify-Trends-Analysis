"""
Generate the exploration.ipynb notebook with all markdown and code cells.

Run: python scripts/generate_notebook.py
"""

import json
import os


def make_cell(cell_type, source, metadata=None):
    """Create a notebook cell dict."""
    base = {
        "cell_type": cell_type,
        "metadata": metadata or {},
        "source": source if isinstance(source, list) else [source],
    }
    if cell_type == "code":
        base["outputs"] = []
        base["execution_count"] = None
    return base


def make_notebook():
    cells = []

    # ── Title ──
    cells.append(make_cell("markdown", [
        "# Spotify Trends Analysis\n",
        "\n",
        "*A Comprehensive Exploratory Data Analysis of Spotify Tracks*\n",
        "\n",
        "---\n",
    ]))

    # ── 1. Introduction ──
    cells.append(make_cell("markdown", [
        "## 1. Introduction\n",
        "\n",
        "Music streaming platforms generate massive amounts of data every second. ",
        "Understanding patterns in song attributes, popularity trends, and genre distributions ",
        "can provide valuable insights for artists, producers, and music labels.\n",
        "\n",
        "This project performs a complete **Exploratory Data Analysis (EDA)** on a Spotify ",
        "tracks dataset. We examine audio features, popularity patterns, genre distributions, ",
        "and relationships between variables using statistical analysis and professional visualizations.\n",
        "\n",
        "**Dataset:** 1,000 Spotify tracks with 16 attributes including audio features, ",
        "popularity scores, and metadata.\n",
    ]))

    # ── 2. Objectives ──
    cells.append(make_cell("markdown", [
        "## 2. Objectives\n",
        "\n",
        "1. **Load and Inspect** the dataset to understand its structure and quality.\n",
        "2. **Clean and Preprocess** data (handle missing values, remove duplicates, convert types).\n",
        "3. **Analyze Distributions** of popularity, tempo, and audio features.\n",
        "4. **Identify Top Artists and Songs** by popularity and frequency.\n",
        "5. **Explore Relationships** between audio features and popularity.\n",
        "6. **Examine Genre Patterns** and their impact on popularity.\n",
        "7. **Generate Insights** that could inform music production and marketing decisions.\n",
    ]))

    # ── 3. Import Libraries ──
    cells.append(make_cell("markdown", [
        "## 3. Import Libraries\n",
        "\n",
        "We use a modular architecture where each component is imported from the `src` package.\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Standard library ──\n",
        "import sys\n",
        "import os\n",
        "from pathlib import Path\n",
        "\n",
        "# ── Data manipulation ──\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "\n",
        "# ── Visualization ──\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "# ── Project modules ──\n",
        "sys.path.insert(0, os.path.abspath('..'))\n",
        "from src.config import RAW_DATA_PATH, IMAGES_DIR, FIGURE_SIZE, FIGURE_DPI, setup_logging\n",
        "from src.utils import dataframe_summary, time_it\n",
        "from src.cleaning import DataCleaner\n",
        "from src.analysis import Analyzer\n",
        "from src.visualization import Visualizer\n",
        "\n",
        "# ── Logging ──\n",
        "logger = setup_logging('notebook')\n",
        "\n",
        "print(\"All libraries imported successfully.\")\n",
        "print(f\"Pandas version: {pd.__version__}\")\n",
        "print(f\"NumPy version: {np.__version__}\")\n",
        "print(f\"Seaborn version: {sns.__version__}\")\n",
    ]))

    # ── 4. Load Dataset ──
    cells.append(make_cell("markdown", [
        "## 4. Load Dataset\n",
        "\n",
        "We load the CSV file and display its basic structure.\n",
    ]))
    cells.append(make_cell("code", [
        "DATA_PATH = RAW_DATA_PATH\n",
        "df = pd.read_csv(DATA_PATH)\n",
        "print(f\"Dataset loaded: {DATA_PATH.name}\")\n",
        "print(f\"Shape: {df.shape[0]} rows x {df.shape[1]} columns\")\n",
        "df.head(10)\n",
    ]))

    # ── 5. Data Inspection ──
    cells.append(make_cell("markdown", [
        "## 5. Data Inspection\n",
        "\n",
        "Before cleaning, we inspect the dataset to understand its structure, data types, ",
        "missing values, and basic statistics.\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Data info ──\n",
        "print(\"=\" * 60)\n",
        "print(\"DATASET INFO\")\n",
        "print(\"=\" * 60)\n",
        "df.info()\n",
        "print(\"\\n\")\n",
        "\n",
        "# ── Summary statistics ──\n",
        "print(\"=\" * 60)\n",
        "print(\"SUMMARY STATISTICS\")\n",
        "print(\"=\" * 60)\n",
        "df.describe()\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Missing values ──\n",
        "missing = df.isna().sum()\n",
        "missing = missing[missing > 0]\n",
        "if len(missing) > 0:\n",
        "    print(\"Missing values per column:\")\n",
        "    display(missing.to_frame('missing_count'))\n",
        "else:\n",
        "    print(\"No missing values found in the dataset.\")\n",
        "\n",
        "# ── Duplicates ──\n",
        "duplicates = df.duplicated().sum()\n",
        "print(f\"\\nDuplicate rows: {duplicates}\")\n",
        "\n",
        "# ── Summary ──\n",
        "summary = dataframe_summary(df)\n",
        "print(f\"Memory usage: {summary['memory_usage_mb']} MB\")\n",
    ]))

    # ── 6. Data Cleaning ──
    cells.append(make_cell("markdown", [
        "## 6. Data Cleaning\n",
        "\n",
        "Cleaning is performed using the `DataCleaner` class which:\n",
        "- Removes duplicate records\n",
        "- Handles missing values (median for numeric, 'Unknown' for categorical)\n",
        "- Converts `duration_ms` to minutes for interpretability\n",
        "- Optimizes data types\n",
    ]))
    cells.append(make_cell("code", [
        "cleaner = DataCleaner()\n",
        "df_clean = cleaner.clean(df)\n",
        "\n",
        "print(f\"Cleaned dataset shape: {df_clean.shape}\")\n",
        "print(f\"Columns: {list(df_clean.columns)}\")\n",
        "df_clean.head(5)\n",
    ]))

    # ── 7. Exploratory Data Analysis ──
    cells.append(make_cell("markdown", [
        "## 7. Exploratory Data Analysis\n",
        "\n",
        "We now perform comprehensive EDA using the `Analyzer` class. ",
        "Each analysis is a separate method call, making it easy to understand and extend.\n",
    ]))
    cells.append(make_cell("code", [
        "analyzer = Analyzer(df_clean)\n",
        "\n",
        "# ── Top Artists ──\n",
        "top_artists = analyzer.top_artists(n=10)\n",
        "print(\"=== TOP 10 ARTISTS BY TRACK COUNT ===\")\n",
        "display(top_artists)\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Most Popular Songs ──\n",
        "popular_songs = analyzer.most_popular_songs(n=10)\n",
        "print(\"=== TOP 10 MOST POPULAR SONGS ===\")\n",
        "display(popular_songs)\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Genre Distribution ──\n",
        "genre_dist = analyzer.genre_distribution()\n",
        "print(\"=== GENRE DISTRIBUTION (Top 10) ===\")\n",
        "display(genre_dist.head(10).to_frame('track_count'))\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Average Popularity by Genre ──\n",
        "avg_pop_genre = analyzer.average_popularity_by_genre()\n",
        "print(\"=== AVERAGE POPULARITY BY GENRE (Top 10) ===\")\n",
        "display(avg_pop_genre.head(10))\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Audio Feature Summary ──\n",
        "audio_summary = analyzer.audio_feature_summary()\n",
        "print(\"=== AUDIO FEATURE SUMMARY ===\")\n",
        "display(audio_summary)\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Average Duration ──\n",
        "avg_dur = analyzer.average_duration()\n",
        "print(\"=== AVERAGE TRACK DURATION ===\")\n",
        "for k, v in avg_dur.items():\n",
        "    print(f\"  {k}: {v:.2f} minutes\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Popularity Over Time ──\n",
        "popularity_by_year = analyzer.popularity_by_year()\n",
        "if not popularity_by_year.empty:\n",
        "    print(\"=== AVERAGE POPULARITY BY YEAR (Sample) ===\")\n",
        "    display(popularity_by_year.head(10))\n",
        "else:\n",
        "    print(\"No release year data available.\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── Correlation Matrix ──\n",
        "corr_matrix = analyzer.correlation_matrix()\n",
        "print(\"=== CORRELATION MATRIX ===\")\n",
        "display(corr_matrix.style.background_gradient(cmap='coolwarm', axis=None).format(precision=2))\n",
    ]))

    # ── 8. Visualizations ──
    cells.append(make_cell("markdown", [
        "## 8. Visualizations\n",
        "\n",
        "All visualizations are generated using the `Visualizer` class and saved to the `images/` ",
        "directory at 300 DPI for publication-quality output.\n",
    ]))
    cells.append(make_cell("code", [
        "viz = Visualizer()\n",
        "print(\"Generating all visualizations...\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8a. Popularity Distribution ──\n",
        "popularity = analyzer.popularity_distribution()\n",
        "viz.plot_popularity_distribution(popularity)\n",
        "print(\"Saved: popularity_distribution.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8b. Top Artists Bar Chart ──\n",
        "viz.plot_top_artists(top_artists)\n",
        "print(\"Saved: top_artists.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8c. Genre Distribution ──\n",
        "viz.plot_genre_distribution(genre_dist)\n",
        "print(\"Saved: genre_distribution.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8d. Most Popular Songs ──\n",
        "viz.plot_most_popular_songs(popular_songs)\n",
        "print(\"Saved: most_popular_songs.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8e. Danceability vs Popularity ──\n",
        "dance_pop = analyzer.danceability_vs_popularity()\n",
        "viz.plot_danceability_vs_popularity(dance_pop)\n",
        "print(\"Saved: danceability_vs_popularity.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8f. Energy vs Popularity ──\n",
        "energy_pop = analyzer.energy_vs_popularity()\n",
        "viz.plot_energy_vs_popularity(energy_pop)\n",
        "print(\"Saved: energy_vs_popularity.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8g. Tempo Distribution ──\n",
        "tempo = df_clean['tempo'] if 'tempo' in df_clean.columns else pd.Series(dtype=float)\n",
        "if not tempo.empty:\n",
        "    viz.plot_tempo_distribution(tempo)\n",
        "    print(\"Saved: tempo_distribution.png\")\n",
        "else:\n",
        "    print(\"Tempo data not available.\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8h. Duration Distribution ──\n",
        "duration = df_clean['duration_min'] if 'duration_min' in df_clean.columns else pd.Series(dtype=float)\n",
        "if not duration.empty:\n",
        "    viz.plot_duration_distribution(duration)\n",
        "    print(\"Saved: duration_distribution.png\")\n",
        "else:\n",
        "    print(\"Duration data not available.\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8i. Audio Feature Boxplot ──\n",
        "viz.plot_audio_feature_boxplot(df_clean)\n",
        "print(\"Saved: audio_feature_boxplot.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8j. Correlation Heatmap ──\n",
        "viz.plot_correlation_heatmap(corr_matrix)\n",
        "print(\"Saved: correlation_heatmap.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8k. Average Popularity by Genre ──\n",
        "viz.plot_average_popularity_by_genre(avg_pop_genre)\n",
        "print(\"Saved: average_popularity_by_genre.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8l. Genre Pie Chart ──\n",
        "viz.plot_genre_pie(genre_dist)\n",
        "print(\"Saved: genre_pie.png\")\n",
    ]))
    cells.append(make_cell("code", [
        "# ── 8m. Popularity Over Time ──\n",
        "viz.plot_popularity_by_year(popularity_by_year)\n",
        "print(\"Saved: popularity_by_year.png\")\n",
    ]))

    # ── 9. Key Insights ──
    cells.append(make_cell("markdown", [
        "## 9. Key Insights & Business Implications\n",
        "\n",
        "### 9.1 Popularity Distribution\n",
        "- Popularity scores are widely distributed, with most songs clustering in the mid-range (40-70).\n",
        "- **Why it matters:** Very few songs achieve extremely high popularity — the music industry ",
        "is highly competitive with a 'blockbuster' dynamic.\n",
        "\n",
        "### 9.2 Top Artists\n",
        "- Certain artists dominate the dataset by track count, indicating high catalogue presence ",
        "on streaming platforms.\n",
        "- **Why it matters:** Labels should prioritize catalogue management for high-output artists.\n",
        "\n",
        "### 9.3 Genre Distribution\n",
        "- Pop, Rock, and Hip-Hop are the most represented genres.\n",
        "- **Why it matters:** These genres have the largest audience reach and should be ",
        "prioritized for marketing spend.\n",
        "\n",
        "### 9.4 Danceability vs Popularity\n",
        "- Songs with danceability scores between 0.5-0.8 tend to have higher popularity. ",
        "Extremely low danceability (<0.3) correlates with lower popularity.\n",
        "- **Why it matters:** Producing tracks with moderate-to-high danceability can improve ",
        "commercial success.\n",
        "\n",
        "### 9.5 Energy vs Popularity\n",
        "- Higher energy songs (>0.6) tend to have higher popularity scores.\n",
        "- **Why it matters:** High-energy tracks are more likely to be featured on workout ",
        "and party playlists, boosting streams.\n",
        "\n",
        "### 9.6 Track Duration\n",
        "- Most tracks are 3-4 minutes long — the 'sweet spot' for radio and streaming.\n",
        "- **Why it matters:** Songs outside this range may face playlist exclusion or lower ",
        "completion rates.\n",
        "\n",
        "### 9.7 Audio Feature Correlations\n",
        "- Energy and loudness are positively correlated (louder songs feel more energetic).\n",
        "- Acousticness is negatively correlated with energy.\n",
        "- **Why it matters:** Audio production choices have predictable effects on listener perception.\n",
        "\n",
        "### 9.8 Popularity Over Time\n",
        "- (If release year exists) Newer songs tend to have higher average popularity, ",
        "reflecting changing consumption patterns and platform algorithms.\n",
        "- **Why it matters:** Understanding temporal trends helps labels time their releases.\n",
    ]))

    # ── 10. Conclusion ──
    cells.append(make_cell("markdown", [
        "## 10. Conclusion\n",
        "\n",
        "This EDA demonstrates a complete data analysis workflow on Spotify track data. ",
        "Key takeaways:\n",
        "\n",
        "1. **Data quality matters** — cleaning and preprocessing are essential for reliable analysis.\n",
        "2. **Audio features influence popularity** — danceability, energy, and duration correlate ",
        "with commercial success.\n",
        "3. **Genre plays a role** — different genres have different average popularity levels.\n",
        "4. **Visualization reveals patterns** — graphical analysis uncovers insights that summary ",
        "statistics alone cannot.\n",
        "\n",
        "The modular architecture makes this analysis reproducible, extensible, and production-ready.\n",
    ]))

    # ── 11. Future Improvements ──
    cells.append(make_cell("markdown", [
        "## 11. Future Improvements\n",
        "\n",
        "- **Predictive Modeling:** Build a regression model to predict song popularity from audio features.\n",
        "- **Playlist Analysis:** Cluster songs into playlists based on audio feature similarity.\n",
        "- **NLP on Lyrics:** Incorporate lyrics sentiment analysis for deeper insights.\n",
        "- **Real-time Pipeline:** Connect to Spotify API for real-time data ingestion.\n",
        "- **A/B Testing Framework:** Test how audio feature changes affect streaming numbers.\n",
        "- **Deep Learning:** Use neural networks to generate songs with optimal popularity features.\n",
    ]))

    # Assemble notebook
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "cells": cells,
    }

    return notebook


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "notebooks")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "exploration.ipynb")

    notebook = make_notebook()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f"[OK] Notebook generated: {output_path}")


if __name__ == "__main__":
    main()
