import streamlit as st
from src.recommender import load_songs, recommend_songs

st.set_page_config(page_title="VibeFinder 1.0", page_icon="🎵", layout="centered")

# Load catalog once and cache it
@st.cache_data
def get_songs():
    return load_songs("data/songs.csv")

songs = get_songs()

# Pull sorted unique values from the catalog for the dropdowns
all_genres = sorted({s["genre"] for s in songs})
all_moods  = sorted({s["mood"]  for s in songs})

# ── Sidebar: user profile ────────────────────────────────────────────────────
st.sidebar.header("Your Taste Profile")

genre        = st.sidebar.selectbox("Favorite genre",  all_genres, index=all_genres.index("pop"))
mood         = st.sidebar.selectbox("Favorite mood",   all_moods,  index=all_moods.index("happy"))
energy       = st.sidebar.slider("Target energy", 0.0, 1.0, 0.80, step=0.01,
                                  help="0 = very quiet/calm, 1 = maximum intensity")
likes_acoustic = st.sidebar.checkbox("I like acoustic songs", value=False)
k            = st.sidebar.slider("How many recommendations?", 1, 10, 5)

user_prefs = {
    "genre": genre,
    "mood": mood,
    "energy": energy,
    "likes_acoustic": likes_acoustic,
}

# ── Main panel ───────────────────────────────────────────────────────────────
st.title("🎵 VibeFinder 1.0")
st.caption("A content-based music recommender — adjust your profile on the left to update results.")

st.divider()

recommendations = recommend_songs(user_prefs, songs, k=k)

if not recommendations:
    st.warning("No songs found. Try adjusting your profile.")
else:
    st.subheader(f"Top {k} picks for: **{genre} / {mood} / energy {energy:.2f}**")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**#{rank} — {song['title']}**  \n*{song['artist']}*")
                st.caption(f"Genre: {song['genre']} · Mood: {song['mood']} · Energy: {song['energy']:.2f}")
            with col2:
                st.metric("Score", f"{score:.2f}")
            st.markdown(f"**Why:** {explanation}")

st.divider()

with st.expander("Browse full catalog"):
    import pandas as pd
    df = pd.DataFrame(songs)[["title", "artist", "genre", "mood", "energy", "acousticness"]]
    df.columns = ["Title", "Artist", "Genre", "Mood", "Energy", "Acousticness"]
    st.dataframe(df, use_container_width=True, hide_index=True)
