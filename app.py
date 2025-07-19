import streamlit as st
import chromadb
from core.database import add_chapter_version

# App Configuration
st.set_page_config(layout="wide", page_title="Book Publication Workflow")
CHAPTER_NUMBER = 1

# Database & State Management
@st.cache_resource
def get_db_collection():
    """Connects to ChromaDB and returns the collection object."""
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection(name="book_chapters")

def load_versions_into_state(collection):
    """Load all versions for a chapter into the session state once."""
    if 'versions' not in st.session_state:
        st.session_state.versions = {}
        try:
            results = collection.get(
                where={"chapter_id": {"$eq": CHAPTER_NUMBER}},
                include=["documents", "metadatas"]
            )
            # Store the latest of each version type found in the database
            for doc, meta in zip(results['documents'], results['metadatas']):
                st.session_state.versions[meta['version_type']] = doc
        except Exception as e:
            st.error(f"Failed to load versions from database: {e}")

# UI Rendering Functions
def render_editor_tab():
    st.header("Chapter Editor")
    versions = st.session_state.get('versions', {})
    original_text = versions.get('original', "Original text not found.")
    ai_text = versions.get('ai_reviewed', "AI-reviewed text not found.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Reference: Original Text")
        st.markdown(f'<div style="height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{original_text}</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("Editable Version")
        edited_text = st.text_area(
            "Edit the AI-reviewed text:",
            value=ai_text,
            height=500,
            label_visibility="collapsed"
        )
        
        if st.button("Submit Final Version", use_container_width=True, type="primary"):
            if edited_text and edited_text != ai_text:
                add_chapter_version(edited_text, "human_final", CHAPTER_NUMBER)
                st.session_state.message = "Final version saved successfully!"
                del st.session_state.versions 
                st.rerun()
            else:
                st.warning("No changes were made to the text.")

def render_history_tab():
    st.header("Version Comparison")
    versions = st.session_state.get('versions', {})
    version_names = list(versions.keys())

    if len(version_names) < 2:
        st.info("At least two versions are needed for comparison.")
        return

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        left_version_name = st.selectbox("Select Left Version", options=version_names, index=0)
    with col2:
        right_index = 1 if len(version_names) > 1 else 0
        right_version_name = st.selectbox("Select Right Version", options=version_names, index=right_index)
    
    st.divider()

    text_col1, text_col2 = st.columns(2, gap="large")
    with text_col1:
        st.subheader(f"Version: {left_version_name}")
        st.markdown(f'<div style="height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{versions.get(left_version_name, "")}</div>', unsafe_allow_html=True)
    with text_col2:
        st.subheader(f"Version: {right_version_name}")
        st.markdown(f'<div style="height: 500px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{versions.get(right_version_name, "")}</div>', unsafe_allow_html=True)

# Main
st.title("Book Publication Workflow")
if "message" in st.session_state:
    st.success(st.session_state.message)
    del st.session_state.message

collection = get_db_collection()
if collection:
    load_versions_into_state(collection)
    
    editor_tab, history_tab = st.tabs(["Editor", "Version History"])
    
    with editor_tab:
        render_editor_tab()
    
    with history_tab:
        render_history_tab()
else:
    st.error("Database connection could not be established.")