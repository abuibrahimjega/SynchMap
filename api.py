from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pyttsx3
import cv2
import numpy as np
import os
import uuid
from typing import Optional

app = FastAPI(title="Multi-Function API")

# Text to Speech Models
class SpeechRequest(BaseModel):
    text: str
    rate: Optional[int] = 150
    volume: Optional[float] = 1.0

# Text to Speech Functions
def init_engine():
    engine = pyttsx3.init()
    return engine

def say(text: str, rate: int = 150, volume: float = 1.0):
    try:
        engine = init_engine()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        print(f"Speaking at rate {engine.getProperty('rate')}")
        print(f"Volume is set to {engine.getProperty('volume')}")
        
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        return {"status": "success", "message": "Text spoken successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Text to Speech Endpoints
@app.post("/speak")
async def speak_text(request: SpeechRequest):
    """
    Convert text to speech with customizable rate and volume.
    
    - **text**: The text to be spoken
    - **rate**: Speech rate (words per minute), default 150
    - **volume**: Volume level (0.0 to 1.0), default 1.0
    """
    return say(request.text, request.rate, request.volume)

# Image Denoising Endpoints
@app.post("/denoise")
async def denoise_image(
    file: UploadFile = File(...),
    h: Optional[int] = 11,
    hColor: Optional[int] = 6,
    templateWindowSize: Optional[int] = 7,
    searchWindowSize: Optional[int] = 21
):
    """
    Denoise an image using Fast Non-Local Means Denoising.
    
    Parameters:
    - file: The image file to denoise
    - h: Parameter regulating filter strength for luminance component
    - hColor: Parameter regulating filter strength for color component
    - templateWindowSize: Size in pixels of the template patch
    - searchWindowSize: Size in pixels of the window used to compute weighted average
    """
    try:
        # Create a unique filename for the uploaded image
        file_extension = os.path.splitext(file.filename)[1]
        input_filename = f"temp_{uuid.uuid4()}{file_extension}"
        output_filename = f"denoised_{uuid.uuid4()}{file_extension}"
        
        # Save the uploaded file
        with open(input_filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Read and process the image
        image = cv2.imread(input_filename)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Apply denoising
        dst = cv2.fastNlMeansDenoisingColored(
            image, 
            None, 
            h, 
            hColor, 
            templateWindowSize, 
            searchWindowSize
        )
        
        # Save the denoised image
        cv2.imwrite(output_filename, dst)
        
        # Clean up the input file
        os.remove(input_filename)
        
        # Return the denoised image
        return FileResponse(
            output_filename,
            media_type=f"image/{file_extension[1:]}",
            filename=f"denoised_{file.filename}"
        )
    except Exception as e:
        # Clean up any temporary files in case of error
        if os.path.exists(input_filename):
            os.remove(input_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Multi-Function API is running",
        "endpoints": {
            "/speak": "Convert text to speech",
            "/denoise": "Denoise images"
        }
    }
