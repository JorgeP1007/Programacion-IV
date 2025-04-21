import csv

def load_data():
    data = []
    with open("measles_vaccination_panama.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                "year": int(row["Year"]),
                "coverage": float(row["Coverage"]),
                "region": row.get("Region", "Nacional")
            })
    return data
