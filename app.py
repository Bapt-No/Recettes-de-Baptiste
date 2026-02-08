import streamlit as st
import json
import os

# Configuration de la page pour le mobile
st.set_page_config(page_title="Le Grimoire de Baptiste et Arnaud", layout="wide")

# --- STYLE PERSONNALISÉ (Effet Wahou) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3em;
        background-color: #f0f2f6;
        border: 2px solid #e0e0e0;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        transform: scale(1.02);
    }
    .recipe-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME DE FICHIER ---
DATA_FILE = "recipes.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"categories": ["Apéro", "Entrées", "Plats", "Desserts"], "recipes": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# --- VÉRROU D'ACCÈS ---
if "auth" not in st.session_state:
    st.title("📖 Bienvenue dans le Grimoire")
    pwd = st.text_input("Entrez le code secret de la famille", type="password")
    if pwd == "1234": # Changez votre code ici
        st.session_state.auth = True
        st.rerun()
    else:
        st.stop()

# --- INTERFACE PRINCIPALE ---
st.sidebar.title("👨‍🍳 Menu")

# Gestion des catégories dans la barre latérale
cat_selected = st.sidebar.radio("Nos catégories", data["categories"])

with st.sidebar.expander("⚙️ Gérer les catégories"):
    new_cat = st.text_input("Nouvelle catégorie")
    if st.button("Ajouter"):
        data["categories"].append(new_cat)
        save_data(data)
        st.rerun()

# --- AFFICHAGE DES RECETTES ---
if "view_recipe" not in st.session_state:
    st.session_state.view_recipe = None

if st.session_state.view_recipe is None:
    st.title(f"Pépites : {cat_selected}")
   
    # Filtrer les recettes par catégorie
    filtered_recipes = [r for r in data["recipes"] if r["category"] == cat_selected]
   
    if not filtered_recipes:
        st.info("Aucune recette ici pour le moment. Ajoutez-en une !")
   
    # Affichage en grille de boutons
    cols = st.columns(2) # 2 colonnes pour le mobile
    for i, recipe in enumerate(filtered_recipes):
        with cols[i % 2]:
            if st.button(f"✨ {recipe['title']}", key=recipe['title']):
                st.session_state.view_recipe = recipe
                st.rerun()

    # Bouton pour ajouter une recette
    st.divider()
    with st.expander("➕ Ajouter une nouvelle pépite"):
        with st.form("new_recipe"):
            title = st.text_input("Nom de la recette")
            url = st.text_input("Lien image/vidéo (URL)")
            ingredients = st.text_area("Ingrédients")
            steps = st.text_area("Préparation")
            if st.form_submit_button("Enregistrer la pépite"):
                new_r = {"title": title, "category": cat_selected, "url": url, "ing": ingredients, "prep": steps}
                data["recipes"].append(new_r)
                save_data(data)
                st.success("C'est enregistré !")
                st.rerun()

else:
    # --- VUE DÉTAILLÉE D'UNE RECETTE ---
    r = st.session_state.view_recipe
    if st.button("⬅️ Retour"):
        st.session_state.view_recipe = None
        st.rerun()
       
    st.title(r["title"])
    if r["url"]:
        st.image(r["url"], use_container_width=True) # Affiche l'image si l'URL est valide
   
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Ingrédients")
        st.write(r["ing"])
    with col2:
        st.subheader("👨‍🍳 Préparation")
        st.write(r["prep"])
   
    if st.button("🗑️ Supprimer cette recette"):
        data["recipes"] = [rec for rec in data["recipes"] if rec["title"] != r["title"]]
        save_data(data)
        st.session_state.view_recipe = None
        st.rerun()
