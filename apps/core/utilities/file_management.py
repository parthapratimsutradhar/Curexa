import os
import hashlib
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

def save_uploaded_file(uploaded_files, subfolder=None):
    """
    Saves one or multiple uploaded files to static/images/<subfolder>/
    Args:
        uploaded_file: In-memory uploaded file.
        subfolder (str): The folder name where the file will be saved.
    
    Returns:
        str: The relative URL path to the saved file.
    """
    if not uploaded_files:
        return []

    # Normalize to list
    if isinstance(uploaded_files, UploadedFile):
        uploaded_files = [uploaded_files]

    base_dir = os.path.join(settings.BASE_DIR, 'static', 'images')

    target_dir = os.path.join(base_dir, subfolder) if subfolder else base_dir
    os.makedirs(target_dir, exist_ok=True)

    saved_paths = []

    for uploaded_file in uploaded_files:

        # Skip already-saved paths
        if isinstance(uploaded_file, str):
            saved_paths.append(uploaded_file)
            continue

        md5_hash = hashlib.md5()
        for chunk in uploaded_file.chunks():
            md5_hash.update(chunk)

        file_hash = md5_hash.hexdigest()
        _, ext = os.path.splitext(uploaded_file.name)
        new_file_name = f"{file_hash}{ext}"
        file_path = os.path.join(target_dir, new_file_name)

        if not os.path.exists(file_path):
            uploaded_file.seek(0)
            with open(file_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

        relative_path = (
            f'/static/images/{subfolder}/{new_file_name}'
            if subfolder
            else f'/static/images/{new_file_name}'
        )

        saved_paths.append(relative_path)

    return saved_paths
