"""Validation helpers."""
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4'
}


def allowed_file(filename: str) -> bool:
    """Check allowed file extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
