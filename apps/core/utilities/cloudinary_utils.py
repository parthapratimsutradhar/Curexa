# apps/medistore/utils/cloudinary_utils.py
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from django.conf import settings

# Cloudinary configuration
cloudinary.config(
    cloud_name=getattr(settings, "CLOUD_NAME", None),
    api_key=getattr(settings, "API_KEY", None),
    api_secret=getattr(settings, "API_SECRET", None),
    secure=True
)

def cloudinary_upload_files(files, folder_name="medicines"):
    """
    Upload multiple files to Cloudinary and return their secure URLs.
    
    Args:
        files (list): List of file objects (from DRF request.FILES)
        folder_name (str): Cloudinary folder path
    
    Returns:
        list: List of secure URLs for uploaded images
    """
    urls = []

    for file in files:
        result = cloudinary.uploader.upload(
            file,
            folder=folder_name,
            use_filename=True,
            unique_filename=True,
            overwrite=False
        )
        # Generate optimized URL (auto format + auto quality)
        optimized_url, _ = cloudinary_url(
            result["public_id"],
            fetch_format="auto",
            quality="auto"
        )
        urls.append(optimized_url)

    return urls
