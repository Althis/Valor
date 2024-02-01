import requests
import csv
from tqdm import tqdm

# Define the API endpoint
url = "https://clob.polymarket.com/"
next_cursor = ""

with open('markets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["question", "description", "category", "active", "closed", "options", "outcome"])

    for i in tqdm(range(0, 1000)):
        response = requests.get(url + f"/markets?next_cursor={next_cursor}")

        data = response.json()

        # Check if 'next_cursor' is in the response
        if 'next_cursor' in data:
            next_cursor = data['next_cursor']
        
        if not 'data' in data:
            print("no data")
            continue

        for market in data['data']:
            if market['closed']:
                tokens = market['tokens']
                options = [token['outcome'] for token in tokens]
                outcome = None
                for token in tokens:
                    if 'winner' in token and token['winner']:
                        outcome = token['outcome']
                        break
                writer.writerow([market['question'], market['description'], market['categories'], market['active'], market['closed'], options, outcome])
            else:
                continue
        # Break the loop if there is no next_cursor
        if not next_cursor:
            break