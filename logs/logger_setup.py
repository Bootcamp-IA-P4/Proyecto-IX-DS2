import logging
import os

def setup_logging():
    path = os.path.dirname(os.path.abspath(__file__))
    logs_path = os.path.join(path, 'logs.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(logs_path)]
    )

# Reducir logs muy verbosos de librerías externas (ejemplo uvicorn)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("supabase").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)
