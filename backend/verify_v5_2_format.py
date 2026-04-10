import requests
import json

def test_v5_2_format():
    url = "http://localhost:8000/chat"
    payload = {
        "session_id": "test-v5-2-format",
        "message": "Red dots on skin and itching",
    }
    
    print(f"Sending request: {payload['message']}")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("response", "")
            print("\n--- Wellora Unified Format V5.2 Check ---")
            
            headers = [
                "🔎 What You Shared",
                "🧠 Possible Causes (Ranked)",
                "💊 Care & Medicine Category",
                "⏳ When to Seek Medical Help",
                "📊 AI Confidence"
            ]
            
            missing = []
            for h in headers:
                if h in content:
                    print(f"✅ Found Header: {h}")
                else:
                    print(f"❌ Missing Header: {h}")
                    missing.append(h)
            
            print("\n--- Full Response Preview ---")
            print(content[:500] + "...")
            
            if not missing:
                print("\nSUCCESS: All V5.2 headers are present.")
            else:
                print(f"\nFAILURE: Missing headers: {missing}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_v5_2_format()
