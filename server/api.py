from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import openai
from db import SessionLocal, Translation
from llm import translate_text
from pydantic import BaseModel
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import pandas as pd
from tqdm import tqdm

class TranslateRequest(BaseModel):
    input_text: str

def load_and_index_data():
    try:
        # Load the CSV file
        df = pd.read_csv('./data/content.csv')[:100]

        # Prepare and index the data
        embeddings = []
        metadatas = []
        ids = []

        # Use tqdm to track progress
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Indexing data"):
            sentence = row['문장']
            description = row['혐오내용설명']
            
            embedding = model.encode(sentence, normalize_embeddings=True).tolist()
            metadata = {"sentence": sentence, "description": description}
            
            embeddings.append(embedding)
            metadatas.append(metadata)
            ids.append(str(index))

        # Add data to ChromaDB collection
        collection.add(embeddings=embeddings, ids=ids, metadatas=metadatas)
        print("Data loaded and indexed successfully.")
    except Exception as e:
        print(f"Error loading and indexing data: {str(e)}")
        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
router = APIRouter()
client = PersistentClient(path="./data")
collection = client.get_or_create_collection(name="sentences")  
model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
load_and_index_data()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    # Check Database Connection
    try:
        # Simple query to ensure the database is accessible
        db.execute(text("SELECT 1"))
        db_status = "Database is connected"
        print("Database connection successful.")
    except OperationalError:
        db_status = "Database is not connected"
        print("Failed to connect to the database.")
    
    # Check OpenAI API
    try:
        # Initialize the OpenAI client
        models = openai.models.list()  # A simple call to check if the API is reachable
        print(f"OpenAI models: {models}")
        openai_status = "OpenAI API is accessible"
        print("OpenAI API connection successful.")
    except Exception as e:
        openai_status = f"OpenAI API is not accessible: {str(e)}"
        print(f"Failed to connect to OpenAI API: {str(e)}")
    
    print("Health check completed.")
    
    return {
        "status": "Server is running",
        "database": db_status,
        "openai": openai_status
    }@router.post("/translate")

@router.post("/translate")
async def translate(request: TranslateRequest, db: Session = Depends(get_db)):
    input_text = request.input_text
    print("Received translation request.")
    print(f"Input text: {input_text}")

    similar_sentences_list = []

    # Step 1: Query ChromaDB for similar sentences (RAG part)
    try:
        query_embedding = model.encode(input_text, normalize_embeddings=True).tolist()
        result = collection.query(query_embeddings=[query_embedding], n_results=3)
        print(result)
        if result['ids'][0]:
            print("Similar sentences found in ChromaDB.")
            similar_sentences = result['metadatas'][0]
            
            # Create a string with the format: "sentence는 description이다."
            concatenated_similar_sentences = ' '.join([
                f"{sentence['sentence']}는 {sentence['description']}이다."
                for sentence in similar_sentences
            ])

            # Prepare a list of the similar sentences
            similar_sentences_list = [[sentence['sentence']] for sentence in similar_sentences]
            
            print(f"Concatenated similar sentences: {concatenated_similar_sentences}")
        else:
            print("No similar sentences found.")
            concatenated_similar_sentences = None
    except Exception as e:
        print(f"Error querying ChromaDB: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to query ChromaDB")

    # Step 2: Translate the input text using OpenAI
    try:
        if concatenated_similar_sentences:
            # Optionally, use the concatenated similar sentences directly as the translation
            translated_text = translate_text(input_text, concatenated_similar_sentences)
            print(f"Translated text: {translated_text}")
        else:
            translated_text = translate_text(input_text, "")
            print(f"Translated text: {translated_text}")
    except Exception as e:
        print(f"Error during translation: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation failed")

    # Step 3: Split both input and translated text by '.'
    input_sentences = [sentence.strip() for sentence in input_text.split('.') if sentence.strip()]
    output_sentences = [sentence.strip() for sentence in translated_text.split('.') if sentence.strip()]
    print(f"Input sentences: {input_sentences}")
    print(f"Output sentences: {output_sentences}")

    # Step 4: Compare and identify differences
    isdiff = [index for index, (i, o) in enumerate(zip(input_sentences, output_sentences)) if i != o]
    print(f"Changed indices (isdiff): {isdiff}")

    # Step 5: Save the input and output to the database
    try:
        translation = Translation(input_text=input_text, output_text=translated_text)
        db.add(translation)
        db.commit()
        db.refresh(translation)
        print("Translation saved to database.")
    except Exception as e:
        print(f"Error saving translation to database: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save translation to database")

    # Step 6: Return the response
    response = {
        "strings": output_sentences,
        "isdiff": isdiff,
        "similar_sentences": similar_sentences_list  # Return the list of similar sentences
    }
    print(f"Response: {response}")
    return response


@router.get("/translations")
async def get_translations(db: Session = Depends(get_db)):
    try:
        # Fetch all translations from the database
        translations = db.query(Translation).all()
        print(f"Fetched {len(translations)} translations from the database.")
        return [{"id": t.id, "input_text": t.input_text, "output_text": t.output_text, "created_at": t.created_at} for t in translations]
    except Exception as e:
        print(f"Error fetching translations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch translations")