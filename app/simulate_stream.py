import pandas as pd
import time
import random
from datetime import datetime

file_path = "../data/hospital_stream.csv"

hospitals = [
    (1, "City Hospital", "Bangalore", 12.9716, 77.5946),
    (2, "Care Hospital", "Bangalore", 12.9352, 77.6245),
    (3, "LifeLine Hospital", "Bangalore", 12.9081, 77.6476),
]

while True:
    hospital = random.choice(hospitals)

    new_row = {
    "hospital_id": hospital[0],
    "hospital_name": hospital[1],
    "city": hospital[2],
    "latitude": hospital[3],
    "longitude": hospital[4],
    "icu_beds": random.randint(0, 10),
    "oxygen_beds": random.randint(0, 20),
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}


    df = pd.DataFrame([new_row])
    df.to_csv(file_path, mode="a", header=False, index=False)

    print("New update added:", new_row)
    time.sleep(5)
