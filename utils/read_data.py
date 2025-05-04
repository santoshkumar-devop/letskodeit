import csv

def getCSVData(filepath):
    test_data = []
    try:
        with open(filepath, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                test_data.append(row)
        return test_data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return []