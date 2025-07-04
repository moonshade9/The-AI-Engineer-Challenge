from aimakerspace.text_utils import ImageLoader
import os

# Create sample image files for testing
sample_base_path = "tests/sample_test"
formats = ["png", "jpg", "jpeg"]

# Only create the images if they don't exist
for ext in formats:
    path = f"{sample_base_path}.{ext}"
    if not os.path.exists(path):
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (200, 60), color = (255, 255, 255))
            d = ImageDraw.Draw(img)
            text = f"Test {ext.upper()}"
            d.text((10, 10), text, fill=(0, 0, 0))
            img.save(path)
        except ImportError:
            print("Pillow is required to generate sample images. Please install it with 'uv pip install pillow'.")
            exit(1)

# Test the ImageLoader for each format
for ext in formats:
    path = f"{sample_base_path}.{ext}"
    print(f"\nTesting ImageLoader with {path}:")
    loader = ImageLoader(path)
    loader.load()
    docs = loader.documents
    print("Loaded documents (OCR output):")
    for doc in docs:
        print(doc) 