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
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = ort.InferenceSession("Backend\\model1.onnx")

def preprocess_image(image):
    image = image.resize((150, 150)) 
    image = np.array(image).astype(np.float32) / 255.0 
    
    image = np.expand_dims(image, axis=0)  
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    print(f"Received file content type: {file.content_type}")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image = Image.open(BytesIO(await file.read())).convert("RGB")
        input_data = preprocess_image(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    inputs = {session.get_inputs()[0].name: input_data}
    prediction = session.run(None, inputs)

    return JSONResponse(content={"prediction": prediction[0].tolist()})
