from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import tensorflow as tf
import logging
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Initialize the Keras model
model = tf.keras.models.load_model('model.h5')

# Configure logging
logging.basicConfig(level=logging.DEBUG)


# Define a function to fetch specific fields from Firestore document
def fetch_fields(doc):
    return {
        'place_id': doc.id,
        'name': doc.get('name'),
        'rating': doc.get('rating'),
        'reviews_count': doc.get('reviews_count'),
        'address': doc.get('address'),
        'lat': doc.get('lat'),
        'long': doc.get('long'),
        'category': doc.get('category'),
        'image_url': f"http://34.101.153.83:3000/img/{doc.id}.jpg",
        'caption_idn': doc.get('caption_idn'),
        'caption_eng': doc.get('caption_eng')
    }


# Define a function to fetch specific fields from Firestore document
def fetch_lon_lat(doc):
    return {
        'place_id': doc.id,
        'name': doc.get('name'),
        'lat': doc.get('lat'),
        'long': doc.get('long')
    }


# Mount the static files directory
app.mount("/img", StaticFiles(directory="img"), name="img")


@app.get("/")
def read_root():
    return {"REST API for Journey on Solo"}


@app.get("/data")
async def get_data():
    try:
        collection_ref = db.collection('location')
        docs = collection_ref.stream()
        formatted_data = []
        for doc in docs:
            data = fetch_fields(doc)
            formatted_data.append(data)
        return formatted_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{place_id}")
async def get_detail_data(place_id: str):
    try:
        collection_ref = db.collection('location')
        query_ref = collection_ref.where('place_id', '==', place_id).limit(1).get()
        for doc in query_ref:
            data = fetch_fields(doc)
            return data
        raise HTTPException(status_code=404, detail=f"Document with place_id '{place_id}' not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/coordinates")
async def get_all_coordinates():
    try:
        collection_ref = db.collection('location')
        docs = collection_ref.stream()
        coordinates = []
        for doc in docs:
            data = fetch_lon_lat(doc)
            coordinates.append(data)
        return coordinates

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/coordinates/{place_id}")
async def get_coordinates(place_id: str):
    try:
        collection_ref = db.collection('location')
        query_ref = collection_ref.where('place_id', '==', place_id).limit(1).get()
        for doc in query_ref:
            data = fetch_lon_lat(doc)
            return data
        raise HTTPException(status_code=404, detail=f"Document with place_id '{place_id}' not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
async def search_data(name: Optional[str] = Query(None, description="Name to search for")):
    try:
        logging.debug(f"Search query parameter: name='{name}'")
        collection_ref = db.collection('location')
        query = collection_ref
        if name:
            query = query.where('name', '==', name)
        docs = query.stream()
        raw_docs = list(docs)
        logging.debug(f"Raw documents fetched: {raw_docs}")
        results = []
        for doc in raw_docs:
            data = fetch_fields(doc)
            results.append(data)
        logging.debug(f"Search results: {results}")
        if not results:
            logging.debug("No documents matched the query.")
        return results

    except Exception as e:
        logging.error(f"Error during search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
async def predict(request: Request):
    try:
        data = await request.json()
        if 'features' not in data:
            return JSONResponse(status_code=400, content={"error": "'features' key not found in the request data"})
        features = data['features']
        input_data = np.array([features])
        predictions = model.predict(input_data)
        predicted_class = np.argmax(predictions, axis=1).tolist()
        return {"predictions": predicted_class}

    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
