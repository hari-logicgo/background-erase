from gradio_client import Client, handle_file
from app.config import HF_SPACE

client = Client(HF_SPACE)

def remove_bg(image_path: str):
    """
    Call HF Space to remove background
    """
    result = client.predict(
        f=handle_file(image_path),
        api_name="/png"
    )
    return result
