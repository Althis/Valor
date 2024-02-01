import csv

with open('markets.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Open the output files
    with open('simplequestions.txt', 'w', encoding='utf-8') as simple_file, open('extendedquestions.txt', 'w', encoding='utf-8') as extended_file, open('taggedsimplequestions.txt', 'w', encoding='utf-8') as tagged_simple_file, open('taggedextendedquestions.txt', 'w', encoding='utf-8') as tagged_extended_file:
        for row in csv_reader:
            # Extract the required columns
            question = row['question']
            description = row['description'].replace('\n', ' ')
            category = row['category']
            options = row['options']
            outcome = row['outcome']

            simple_file.write(f"{question} {options}\n")
            extended_file.write(f"{question} {description} {options}\n")
            tagged_simple_file.write(f"QUESTION: {question} OPTIONS: {options}\n")
            tagged_extended_file.write(f"QUESTION: {question} {description} OPTIONS: {options}\n")
