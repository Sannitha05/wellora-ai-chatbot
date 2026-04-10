# test_glm.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("ZHIPU_API_KEY") or os.getenv("ZHIPUAI_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

try:
    print(f"Testing with key: {client.api_key[:5]}... and model glm-4.7-flash")
    response = client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[{"role": "user", "content": "I have a fever"}],
        temperature=0.3,
        max_tokens=100
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
