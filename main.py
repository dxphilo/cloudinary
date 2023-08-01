
from fastapi import HTTPException, status, UploadFile, FastAPI
from cloudinary.uploader import upload
from typing import List
import uvicorn
import cloudinary
import asyncio
from config import settings

app = FastAPI()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

@app.get('/health')
def health_check():
    return { 
        'app_name': settings.APP_NAME,
        'status': 'OK'
        }


@app.post('/upload/')
async def handle_image_uplaods(images: List[UploadFile]):
    try:         
        uploaded_image_paths = await upload_image(images)

        return uploaded_image_paths
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


async def upload_image(files:list[UploadFile]):
    try:
        async def upload_file(file):
            file_content = await file.read()
            cloudinary_response = await asyncio.to_thread(upload, file_content)
            return cloudinary_response['secure_url']
        upload_tasks = [upload_file(file) for file in files]
        uploaded_paths = await asyncio.gather(*upload_tasks)
        return uploaded_paths
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error uploading images: {e}")


if __name__ == "__main__":
    port = int(8000)

    app_module = "main:app"
    uvicorn.run(app_module, host="0.0.0.0", port=port, reload=True)
