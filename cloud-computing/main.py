from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
app = FastAPI()

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Define a function to fetch specific fields from Firestore document
def fetch_fields(doc):
    # Extract specific fields from the Firestore document
    return {
        'place_id': doc.id,
        'name': doc.get('name'),
        'rating': doc.get('rating'),
        'reviews_count': doc.get('reviews_count'),
        'long': doc.get('long'),
        'lat': doc.get('lat'),
        'category': doc.get('category'),
        'caption_idn': doc.get('caption_idn'),
        'caption_eng': doc.get('caption_eng')
    }
    
# Define a function to fetch specific fields from Firestore document
def fetch_long_lat(doc):
    # Extract 'long' and 'lat' fields from the Firestore document
    return {
        'long': doc.get('long'),
        'lat': doc.get('lat')
    }
    
# Mount the static files directory
app.mount("/img", StaticFiles(directory="img"), name="img")

@app.get("/data")
async def get_data():
    try:
        collection_ref = db.collection('tourism')
        docs = collection_ref.stream()
        
        # Initialize an empty list to store formatted data
        formatted_data = []
        
        # Iterate over documents and format each one
        for doc in docs:
            data = fetch_fields(doc)
            formatted_data.append(data)
            
        return formatted_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to fetch document fields by place_id
@app.get("/data/{place_id}")
async def get_data_fields(place_id: str):
    try:
        collection_ref = db.collection('tourism')
        
        # Query Firestore for documents where 'place_id' matches
        query_ref = collection_ref.where('place_id', '==', place_id).limit(1).get()
        
        # Check if any documents match the query
        for doc in query_ref:
            data = fetch_fields(doc)
            return data
        
        # If no document found with the given place_id
        raise HTTPException(status_code=404, detail=f"Document with place_id '{place_id}' not found")
    
    except HTTPException:
        # Propagate HTTP exceptions (e.g., 404) as they are
        raise
    
    except Exception as e:
        # Handle other exceptions with a generic 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to fetch only 'long' and 'lat' by place_id
@app.get("/coordinates/{place_id}")
async def get_coordinates(place_id: str):
    try:
        collection_ref = db.collection('tourism')
        
        # Query Firestore for documents where 'place_id' matches
        query_ref = collection_ref.where('place_id', '==', place_id).limit(1).get()
        
        # Check if any documents match the query
        for doc in query_ref:
            # Fetch only 'long' and 'lat' fields
            data = fetch_long_lat(doc)
            return data
        
        # If no document found with the given place_id
        raise HTTPException(status_code=404, detail=f"Document with place_id '{place_id}' not found")
    
    except HTTPException:
        # Propagate HTTP exceptions (e.g., 404) as they are
        raise
    
    except Exception as e:
        # Handle other exceptions with a generic 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(e))