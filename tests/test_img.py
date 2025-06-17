# test para comprobar que se suben archivos y que devuelve los valores esperados
import io
from PIL import Image
from fast_api.api.imgs import predict_image

class DummyUploadFile: # creamos una clase para simular la subida de una imágen
    def __init__(self, filename, file_bytes):
        self.filename = filename
        self.file = io.BytesIO(file_bytes)
    async def read(self):
        self.file.seek(0)
        return self.file.read()

import asyncio

def test_predict_image_valid():
    async def run_test():
        img_bytes = io.BytesIO()
        img = Image.new("RGB", (224, 224), color=(255, 0, 0))
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        file = DummyUploadFile("test.png", img_bytes.read())
        # llamamos a nuestra función predict_image pasándole el archivo simulado
        result = await predict_image(file)

        # comprobamos que devolvemos los 3 outputs esperados
        assert isinstance(result, dict)
        assert "filename" in result
        assert "prediction" in result
        assert result["prediction"] in [0, 1]
        assert 0.0 <= result["probability"] <= 1.0

    asyncio.run(run_test())
