import json
import time

DATA_FILE = "dashboard_hospitals.jsonl"

def load_data():
    hospitals = []
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                hospitals.append(json.loads(line))
    except FileNotFoundError:
        pass
    return hospitals


def hospitals_with_icu():
    data = load_data()
    return [h for h in data if h["icu_beds"] > 0]


if __name__ == "__main__":
    while True:
        print("\n--- Hospital AI Assistant ---")
        print("1. Hospitals with ICU beds available")
        print("2. Refresh")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            results = hospitals_with_icu()
            if not results:
                print("❌ No ICU beds available right now")
            else:
                for h in results:
                    print(f"🏥 {h['hospital_name']} | ICU: {h['icu_beds']} | City: {h['city']}")
        elif choice == "2":
            print("🔄 Refreshed")
        elif choice == "3":
            break
        else:
            print("Invalid option")

        time.sleep(1)
