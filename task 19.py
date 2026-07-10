#!/usr/bin/env python3

# 1. Initialization and Setup
import document_loader
import text_splitter
import embedding_model
import faiss_vector_db
import llm

# 2. Data Preparation Pipeline (Run Once / On Update)
def build_knowledge_base(file_path="/var/data/docs/knowledge_base.txt"):
    # Stage 1: Data Ingestion
    raw_documents = document_loader.load(file_path)
    
    # Stage 2: Text Chunking
    chunks = text_splitter.split(raw_documents, chunk_size=500, overlap=50)
    
    # Stage 3: Embedding Generation
    document_embeddings = embedding_model.embed_batch(chunks)
    
    # Stage 4: Vector Storage
    faiss_vector_db.store(document_embeddings, chunks)
    print("Knowledge base successfully indexed in FAISS.")

# 3. Retrieval and Generation Pipeline (Run per User Query)
def answer_user_query(user_query):
    # Convert query to the same vector space
    query_vector = embedding_model.embed(user_query)
    
    # Stage 5: Retrieval
    # Fetch the top 3 most relevant chunks based on vector similarity
    retrieved_chunks = faiss_vector_db.search(query_vector, top_k=3)
    
    # Stage 6: LLM Response Generation
    # Construct a prompt combining the retrieved knowledge and the original query
    augmented_prompt = f"""
    Use the following retrieved context to answer the user's question accurately.
    
    Context:
    {retrieved_chunks}
    
    User Question: {user_query}
    """
    
    final_response = llm.generate_response(augmented_prompt)
    return final_response

# 4. Execution
build_knowledge_base()
user_input = input("Enter your question: ")
print(answer_user_query(user_input))