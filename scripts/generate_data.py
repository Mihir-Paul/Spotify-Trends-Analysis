"""
Script to generate a realistic Spotify-like dataset for the EDA project.

Run once before using the analysis pipeline:
    python scripts/generate_data.py
"""

import csv
import random
import os
from datetime import datetime

random.seed(42)

TRACKS = [
    ("Blinding Lights", "The Weeknd", "After Hours", ["Pop", "R&B"]),
    ("Shape of You", "Ed Sheeran", "Divide", ["Pop"]),
    ("Bohemian Rhapsody", "Queen", "A Night at the Opera", ["Rock"]),
    ("Stairway to Heaven", "Led Zeppelin", "Led Zeppelin IV", ["Rock"]),
    ("Billie Jean", "Michael Jackson", "Thriller", ["Pop", "Funk"]),
    ("Rolling in the Deep", "Adele", "21", ["Pop", "Soul"]),
    ("Smells Like Teen Spirit", "Nirvana", "Nevermind", ["Grunge", "Rock"]),
    ("Hotel California", "Eagles", "Hotel California", ["Rock"]),
    ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "Uptown Special", ["Pop", "Funk"]),
    ("Lose Yourself", "Eminem", "8 Mile Soundtrack", ["Hip-Hop", "Rap"]),
    ("Thinking Out Loud", "Ed Sheeran", "Divide", ["Pop"]),
    ("Someone Like You", "Adele", "21", ["Pop", "Soul"]),
    ("Humble", "Kendrick Lamar", "DAMN.", ["Hip-Hop", "Rap"]),
    ("Shake It Off", "Taylor Swift", "1989", ["Pop"]),
    ("Wonderwall", "Oasis", "Morning Glory", ["Rock", "Britpop"]),
    ("Yesterday", "The Beatles", "Help!", ["Rock"]),
    ("Imagine", "John Lennon", "Imagine", ["Rock"]),
    ("Purple Rain", "Prince", "Purple Rain", ["Pop", "Rock", "Funk"]),
    ("Smooth", "Santana ft. Rob Thomas", "Supernatural", ["Rock", "Latin"]),
    ("Old Town Road", "Lil Nas X", "7", ["Country", "Hip-Hop"]),
    ("Bad Guy", "Billie Eilish", "When We All Fall Asleep", ["Pop"]),
    ("Sunflower", "Post Malone & Swae Lee", "Spider-Verse", ["Hip-Hop", "Pop"]),
    ("Believer", "Imagine Dragons", "Evolve", ["Rock", "Pop"]),
    ("Shape of My Heart", "Sting", "Ten Summoner's Tales", ["Rock", "Pop"]),
    ("Closer", "The Chainsmokers ft. Halsey", "Collage", ["Pop", "EDM"]),
    ("One Dance", "Drake", "Views", ["Hip-Hop", "Pop"]),
    ("God's Plan", "Drake", "Scorpion", ["Hip-Hop", "Pop"]),
    ("Boogie Wonderland", "Earth Wind & Fire", "I Am", ["Disco", "Funk"]),
    ("Stayin' Alive", "Bee Gees", "Saturday Night Fever", ["Disco"]),
    ("Superstition", "Stevie Wonder", "Talking Book", ["Funk", "Soul"]),
    ("Levitating", "Dua Lipa", "Future Nostalgia", ["Pop", "Disco"]),
    ("Watermelon Sugar", "Harry Styles", "Fine Line", ["Pop"]),
    ("Peaches", "Justin Bieber ft. Daniel Caesar", "Justice", ["Pop", "R&B"]),
    ("Without Me", "Halsey", "Manic", ["Pop"]),
    ("Rockstar", "Post Malone ft. 21 Savage", "Beerbongs & Bentleys", ["Hip-Hop", "Pop"]),
    ("Circles", "Post Malone", "Hollywood's Bleeding", ["Pop", "Rock"]),
    ("HIGHEST IN THE ROOM", "Travis Scott", "Highest in the Room", ["Hip-Hop", "Trap"]),
    ("SICKO MODE", "Travis Scott", "Astroworld", ["Hip-Hop", "Trap"]),
    ("Mood", "24kGoldn ft. Iann Dior", "El Dorado", ["Pop", "Hip-Hop"]),
    ("Dance Monkey", "Tones and I", "Kids", ["Pop"]),
    ("Save Your Tears", "The Weeknd", "After Hours", ["Pop", "Synthwave"]),
    ("Don't Start Now", "Dua Lipa", "Future Nostalgia", ["Pop"]),
    ("Lucid Dreams", "Juice WRLD", "Goodbye & Good Riddance", ["Hip-Hop", "Emo Rap"]),
    ("Congratulations", "Post Malone", "Stoney", ["Hip-Hop", "Pop"]),
    ("Goosebumps", "Travis Scott", "Birds in the Trap", ["Hip-Hop", "Trap"]),
    ("Starboy", "The Weeknd ft. Daft Punk", "Starboy", ["Pop", "R&B"]),
    ("Heat Waves", "Glass Animals", "Dreamland", ["Pop", "Indie"]),
    ("good 4 u", "Olivia Rodrigo", "SOUR", ["Pop", "Rock"]),
    ("drivers license", "Olivia Rodrigo", "SOUR", ["Pop"]),
    ("Montero", "Lil Nas X", "Montero", ["Hip-Hop", "Pop"]),
]

ARTISTS = [
    "The Weeknd", "Ed Sheeran", "Queen", "Led Zeppelin", "Michael Jackson",
    "Adele", "Nirvana", "Eagles", "Mark Ronson", "Eminem",
    "Kendrick Lamar", "Taylor Swift", "Oasis", "The Beatles", "John Lennon",
    "Prince", "Santana", "Lil Nas X", "Billie Eilish", "Post Malone",
    "Imagine Dragons", "Sting", "The Chainsmokers", "Drake", "Earth Wind & Fire",
    "Bee Gees", "Stevie Wonder", "Dua Lipa", "Harry Styles", "Justin Bieber",
    "Halsey", "Travis Scott", "24kGoldn", "Tones and I", "Juice WRLD",
    "Glass Animals", "Olivia Rodrigo", "Bruno Mars", "Lady Gaga", "Rihanna",
    "Coldplay", "Linkin Park", "Beyonce", "Kanye West", "Ariana Grande",
    "Shawn Mendes", "Camila Cabello", "Cardi B", "Megan Thee Stallion", "Doja Cat",
]

ALBUMS = [
    "After Hours", "Divide", "Thriller", "21", "Nevermind", "Hotel California",
    "8 Mile Soundtrack", "DAMN.", "1989", "Morning Glory", "Help!", "Imagine",
    "Purple Rain", "Supernatural", "7", "When We All Fall Asleep", "Spider-Verse",
    "Evolve", "Views", "Scorpion", "I Am", "Talking Book", "Future Nostalgia",
    "Fine Line", "Justice", "Manic", "Astroworld", "SOUR", "Starboy", "Dark Side of the Moon",
    "Back in Black", "Rumours", "Born to Die", "Lemonade", "Anti",
    "Channel Orange", "Blonde", "Currents", "In Rainbows", "OK Computer",
    "Random Access Memories", "Discovery", "Homework", "Human After All",
]

GENRES = [
    "Pop", "Rock", "Hip-Hop", "R&B", "Country", "EDM", "Jazz", "Blues",
    "Classical", "Reggae", "Folk", "Indie", "Metal", "Punk", "Soul", "Funk",
    "Disco", "Latin", "Trap", "Grunge", "Britpop", "Synthwave", "Emo Rap", "K-Pop",
]


def generate_track_data(num_rows=1000) -> list[dict]:
    """Generate a list of realistic Spotify track records."""
    rows = []
    base_year = 2024

    for idx in range(num_rows):
        if idx < len(TRACKS) and random.random() < 0.15:
            track_name, artist_name, album_name, genre_list = TRACKS[idx]
            genre = random.choice(genre_list)
        else:
            track_name = f"Track_{idx}"
            artist_name = random.choice(ARTISTS)
            album_name = random.choice(ALBUMS)
            genre = random.choice(GENRES)

        release_year = random.randint(1950, 2025)
        popularity = max(0, min(100, int(random.gauss(55, 25))))
        danceability = round(random.uniform(0.2, 0.98), 3)
        energy = round(random.uniform(0.1, 0.99), 3)
        speechiness = round(random.uniform(0.02, 0.65), 3)
        acousticness = round(random.uniform(0.0, 0.99), 3)
        instrumentalness = round(random.uniform(0.0, 0.95), 3)
        liveness = round(random.uniform(0.01, 0.8), 3)
        valence = round(random.uniform(0.05, 0.98), 3)
        tempo = round(random.uniform(60.0, 200.0), 2)
        duration_ms = int(random.gauss(240000, 60000))
        duration_ms = max(30000, min(600000, duration_ms))
        loudness = round(random.uniform(-25.0, 0.0), 2)

        rows.append({
            "track_name": track_name,
            "artist_name": artist_name,
            "album_name": album_name,
            "genre": genre,
            "popularity": popularity,
            "danceability": danceability,
            "energy": energy,
            "speechiness": speechiness,
            "acousticness": acousticness,
            "instrumentalness": instrumentalness,
            "liveness": liveness,
            "valence": valence,
            "tempo": tempo,
            "duration_ms": duration_ms,
            "loudness": loudness,
            "release_year": release_year,
        })

    return rows


def save_csv(rows: list[dict], filepath: str) -> None:
    """Save the generated data to a CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] Dataset saved to {filepath} -- {len(rows)} rows")


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    filepath = os.path.join(data_dir, "spotify.csv")
    records = generate_track_data(1000)
    save_csv(records, filepath)
