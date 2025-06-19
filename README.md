# 🎬 Movie Explorer

A sleek and interactive **movie recommendation web app** built using [Streamlit](https://streamlit.io/). Browse movies with posters, view detailed movie info, and discover top 5 recommendations for each title.

> 🔎 Powered by fuzzy search  
> 🖼️ Clickable poster-based UI  
> 🤖 Smart content-based recommendations

---

## 🔧 Features

- 🔍 **Fuzzy Search** – find movies even with typos
- 🎞️ **Poster Gallery** – visual browsing experience
- 🎯 **Recommendations** – top 5 suggestions per movie
- 📋 **Full Details** – cast, crew, rating, duration, language, genres, and more
- 🖱️ **Clickable Posters** – intuitive navigation
- 🧠 **Built with**: Streamlit, Pandas, RapidFuzz

---

## 📁 Folder Structure

```plaintext
movie-app/
├── app.py                   # Main Streamlit application
├── movies.pkl               # Movie data with details and poster URLs
├── recommendations.pkl      # Precomputed recommendations dictionary
├── requirements.txt         # Python dependencies
└── README.md                # This file

```

## 🧰 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/movie-app.git
cd movie-app

```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Run the App
```
streamlit run app.py
```
