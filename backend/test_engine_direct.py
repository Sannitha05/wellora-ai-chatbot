from medical_engine import MedicalEngine
import json

def test_engine_directly():
    engine = MedicalEngine()
    
    queries = [
        "I have high fever and body ache. Could it be Dengue?",
        "Symptoms of Malaria",
        "Rash and fever"
    ]
    
    print("\n--- V5.1 Medicine Lookup Test ---")
    med_queries = ["Paracetamol", "Amoxycillin", "Cetirizine"]
    for mq in med_queries:
        meds = engine.search_medicines(mq, limit=2)
        print(f"Query: {mq} | Found: {len(meds)}")
        for m in meds:
            print(f"  - {m['name']} ({m.get('short_composition1', 'N/A')})")
        print("-" * 30)

if __name__ == "__main__":
    test_engine_directly()
