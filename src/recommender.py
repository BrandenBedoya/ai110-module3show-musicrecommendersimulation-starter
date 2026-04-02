import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes loaded from the catalog."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences used to score and rank songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------------
# Shared scoring logic
# ---------------------------------------------------------------------------

def _score_song_obj(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Scores a Song dataclass against a UserProfile; returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if song.genre == user.favorite_genre:
        score += 3.0
        reasons.append("genre match (+3.0)")

    if song.mood == user.favorite_mood:
        score += 2.0
        reasons.append("mood match (+2.0)")

    energy_pts = round((1 - abs(song.energy - user.target_energy)) * 1.5, 2)
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.2f})")

    if user.likes_acoustic and song.acousticness > 0.6:
        score += 1.0
        reasons.append("acoustic match (+1.0)")

    return round(score, 2), reasons


def _score_song_dict(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Scores a song dict against a user prefs dict; returns (score, explanation string)."""
    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 3.0
        reasons.append("genre match (+3.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 2.0
        reasons.append("mood match (+2.0)")

    target_energy = float(user_prefs.get("energy", 0.5))
    song_energy = float(song.get("energy", 0.5))
    energy_pts = round((1 - abs(song_energy - target_energy)) * 1.5, 2)
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.2f})")

    if user_prefs.get("likes_acoustic", False) and float(song.get("acousticness", 0)) > 0.6:
        score += 1.0
        reasons.append("acoustic match (+1.0)")

    return round(score, 2), " | ".join(reasons)


# ---------------------------------------------------------------------------
# OOP interface (used by tests)
# ---------------------------------------------------------------------------

class Recommender:
    """Ranks songs from a catalog against a UserProfile using a weighted scoring rule."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects ranked by weighted score for the given user."""
        scored = [(song, _score_song_obj(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended to this user."""
        _, reasons = _score_song_obj(user, song)
        return " | ".join(reasons)


# ---------------------------------------------------------------------------
# Functional interface (used by main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of dicts with numeric fields cast to float/int."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs against user_prefs and returns the top-k as (song, score, explanation) tuples."""
    scored = [(song, *_score_song_dict(user_prefs, song)) for song in songs]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
