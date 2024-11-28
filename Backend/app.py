from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import onnxruntime as ort
import numpy as np
from PIL import Image
from io import BytesIO

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load ONNX model
session = ort.InferenceSession("model1.onnx")

# Preprocessing function
def preprocess_image(image):
    image = image.resize((150, 150))  # Resize to the model's input dimensions
    image = np.array(image).astype(np.float32) / 255.0  # Normalize to [0, 1]
    
    # The model expects 5 classes, ensure the input data is correctly preprocessed
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Ensure file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read and preprocess the image
    try:
        image = Image.open(BytesIO(await file.read())).convert("RGB")
        input_data = preprocess_image(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    # Model inference
    inputs = {session.get_inputs()[0].name: input_data}
    prediction = session.run(None, inputs)

    # Return response
    return JSONResponse(content={"prediction": prediction[0].tolist()})
