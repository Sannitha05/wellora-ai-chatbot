import requests
import json

def test_v5_1_csv_integration():
    url = "http://localhost:8000/chat"
    payload = {
        "session_id": "test-v5-1-csv",
        "message": "I have a high fever and body ache. Could it be Dengue?",
        "is_logged_in": False
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response Content:\n{response.json().get('response')}\n")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_v5_1_csv_integration()
