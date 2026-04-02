"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi Study": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
    },
    # Edge case: ambient taste but requesting high energy + acoustic — conflicting signals
    "Conflicted Listener": {
        "genre": "ambient",
        "mood": "euphoric",
        "energy": 0.90,
        "likes_acoustic": True,
    },
}


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Prints a formatted recommendation block for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * 56)
    print(f"  PROFILE: {label}")
    print(f"  {user_prefs['genre']} / {user_prefs['mood']} / energy {user_prefs['energy']} / acoustic={user_prefs['likes_acoustic']}")
    print("=" * 56)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in PROFILES.items():
        print_recommendations(label, prefs, songs)


if __name__ == "__main__":
    main()
