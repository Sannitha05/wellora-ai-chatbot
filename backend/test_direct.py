import asyncio, sys, logging
from image_analysis import analyze_medical_image

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

async def test():
    dummy_b64 = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
    res = await analyze_medical_image(dummy_b64)
    print("DONE")

asyncio.run(test())
