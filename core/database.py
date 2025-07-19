import chromadb
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="book_chapters",
    metadata={"hnsw:space": "cosine"} 
)

def add_chapter_version(text: str, version_type: str, chapter_id: int):
    """
    Adds a new version of a chapter to the ChromaDB collection.

    Args:
        text (str): The text content of the chapter version.
        version_type (str): The type of version (e.g., 'original', 'ai_spun', 'ai_reviewed').
        chapter_id (int): An identifier for the chapter (e.g., 1).
    """
    # Create a unique ID for this specific document.
    doc_id = f"{chapter_id}_{version_type}_{str(uuid.uuid4())[:8]}"
    
    collection.add(
        documents=[text],
        metadatas=[{"version_type": version_type, "chapter_id": chapter_id}],
        ids=[doc_id]
    )
    print(f"Version '{version_type}' saved to DB with ID: {doc_id}")
    return doc_id

def semantic_search(query_text: str, chapter_id: int, n_results: int = 3):
    """Finds similar versions of a chapter using semantic search."""
    print(f"\nPerforming semantic search for chapter {chapter_id}...")
    return collection.query(
        query_texts=[query_text],
        where={"chapter_id": chapter_id}, 
        n_results=n_results
    )