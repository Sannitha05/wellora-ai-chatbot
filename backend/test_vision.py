import asyncio
from image_analysis import analyze_medical_image

async def test():
    # Use a dummy 1x1 black JPEG base64
    dummy_b64 = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
    try:
        print("Analyzing image...")
        result = await analyze_medical_image(dummy_b64)
        print("Result:", result)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(test())
