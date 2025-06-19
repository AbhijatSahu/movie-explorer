import streamlit as st
import pandas as pd
import pickle
from rapidfuzz import process, fuzz

# Page config
st.set_page_config(layout="wide")

# Load data
movies = pd.read_pickle("movies.pkl")
recommendations = pickle.load(open("similar_movies.pkl", "rb"))

# Ensure movie IDs are integers
movies["id"] = movies["id"].astype(int)

# Helper functions
def get_movie_by_id(mid):
    df = movies[movies["id"] == mid]
    return df.iloc[0] if not df.empty else None

def fuzzy_search(query, threshold=70):
    titles = movies["name"].tolist()
    matches = process.extract(query, titles, scorer=fuzz.WRatio, limit=30)
    filtered = [m[0] for m in matches if m[1] >= threshold]
    return movies[movies["name"].isin(filtered)]

def render_movie_info(movie, movie_id):
    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: flex-start;
            align-items: center;
            padding: 10px 0 30px 0;
            border-bottom: 2px solid #eee;
        ">
            <a href="/" target="_self" style="
                font-size: 2.5rem;
                font-weight: 700;
                text-decoration: none;
                color: #1f77b4;
                font-family: 'Segoe UI', sans-serif;
            ">
                🎬 Movie Explorer
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(movie["poster"], use_container_width=True)

    with col2:
        info_pieces = []

        if pd.notna(movie.get('rating')):
            info_pieces.append(f"{movie['rating']}/5")
        if pd.notna(movie.get('Primary language')):
            info_pieces.append(f"{movie['Primary language']}")
        if pd.notna(movie.get('minute')):
            info_pieces.append(f"{int(movie['minute'])} min")
        if pd.notna(movie.get('genres')):
            info_pieces.append(f"{movie['genres']}")
        if pd.notna(movie.get('date')):
            info_pieces.append(f"{int(movie['date'])}")

        info_line = ' ● '.join(info_pieces)

        # Prepare tagline if present
        tagline_html = ""
        if pd.notna(movie.get('tagline')) and str(movie['tagline']).strip() != "":
            tagline_html = f"<p style='font-style: italic; margin-top: -10px;'>{movie['tagline']}</p>"

        # Display centered content
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; align-items: center; height: 100%; min-height: 400px;">
            <div style="text-align: left;">
                <h2>{movie['name']}</h2>
                {tagline_html}
                <p style='font-size: 16px;'>{info_line}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Additional info below
    st.markdown("---")
    st.subheader("Description")
    st.markdown(f"{movie.get('description', 'N/A')}")

    st.markdown("---")
    st.subheader("Cast")

    actors = movie.get("actors", "N/A")
    if pd.notna(actors) and isinstance(actors, str):
        actor_list = [a.strip() for a in actors.split(',') if a.strip()]
        
        st.markdown(f"""
        <div style="max-height: 200px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">
            {''.join(f"<p style='margin: 0 0 5px 0;'>• {actor}</p>" for actor in actor_list)}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("N/A")

    st.markdown("---")
    st.subheader("Crew")
    roles = [
        "Director", "Writer", "Original writer", "Story", "Producer", "Executive producer",
        "Editor", "Composer", "Cinematography", "Camera operator", "Lighting",
        "Makeup", "Hairstyling", "Costume design", "Casting", "Set decoration",
        "Production design", "Art direction", "Special effects", "Visual effects",
        "Choreography", "Stunts", "Songs", "Title design", "Assistant director",
        "Co-director", "Additional directing", "Additional photography", "Sound"
    ]

    crew_lines = []
    for role in roles:
        value = movie.get(role)
        if pd.notna(value) and str(value).strip():
            crew_lines.append(f"<p style='margin: 0 0 5px 0;'><strong>{role}:</strong> {value}</p>")

    if crew_lines:
        st.markdown(f"""
        <div style="max-height: 250px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">
            {''.join(crew_lines)}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("No crew data available.")

    # Recommendations
    st.markdown("---")
    similar = recommendations[recommendations['movieId'] == movie_id]
    similar_movies = similar['similar_movies'].values[0]
    rec_movies = []
    for sim_id, _ in similar_movies:
        if sim_id == movie_id:
            continue
        row = movies.loc[movies['id'] == sim_id]
        if not row.empty:
            rec_movies.append(row.iloc[0])
            if len(rec_movies) == 5:
                break

    if rec_movies:
        st.subheader("Recommendations")
        cols = st.columns(5)
        for i, rec in enumerate(rec_movies):
            with cols[i % 5]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <a href="?page=movie&movie_id={rec['id']}" target="_self" style="text-decoration: none;">
                        <img src="{rec['poster']}" style="width:100%; border-radius: 8px;">
                        <div style="margin-top: 0.5rem;">
                            <button style="background: none; border: none; color: white; text-decoration: none; font-size: 1rem; cursor: pointer;">
                                {rec['name']}
                            </button>
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)

# Query parameters and routing
params = st.query_params
page = params.get("page", "home")
movie_id = params.get("movie_id")

try:
    movie_id = int(movie_id) if movie_id is not None else None
except:
    movie_id = None

if page == "movie" and movie_id is not None:
    movie = get_movie_by_id(movie_id)
    if movie is not None:
        render_movie_info(movie, movie_id)
    else:
        st.error(f"Movie with ID {movie_id} not found.")
else:
    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: flex-start;
            align-items: center;
            padding: 10px 0 30px 0;
            border-bottom: 2px solid #eee;
        ">
            <a href="/" target="_self" style="
                font-size: 2.5rem;
                font-weight: 700;
                text-decoration: none;
                color: #1f77b4;
                font-family: 'Segoe UI', sans-serif;
            ">
                🎬 Movie Explorer
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    query = st.text_input("Search for movies")
    if query:
        df = fuzzy_search(query)
    else:
        df = movies.copy()

    cols = st.columns(5) 
    for idx, movie in df.iterrows():
        with cols[idx % 5]:
            st.markdown(f"""
                <div style="text-align: center;">
                    <a href="?page=movie&movie_id={movie['id']}" target="_self" style="text-decoration: none;">
                        <img src="{movie['poster']}" style="width:100%; border-radius: 8px;">
                        <div style="margin-top: 0.5rem;">
                            <button style="background: none; border: none; color: white; text-decoration: none; font-size: 1rem; cursor: pointer;">
                                {movie['name']}
                            </button>
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)