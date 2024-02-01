import pandas as pd
import ast
import os
import re

# Get all the csv files in the directory
result_files = [f for f in os.listdir('zero_shot_results') if f.endswith('.csv')]

for file in result_files:
    df = pd.read_csv(os.path.join('zero_shot_results', file))
    df = df.iloc[:10]  
    df['proper'] = False
    df = df.fillna("N A")

    # Remove newline, punctuation and special characters, convert to lowercase
    df['response'] = df['response'].apply(lambda x: re.sub(r'\W|\n', ' ', str(x)).lower())

    for i, row in df.iterrows():
        response_words = row['response'].split()
        options = ast.literal_eval(row['options'])

        if len(response_words) > 1 and response_words[0] == 'outcome':
            for option in options:
                if row['response'].find(option.lower()) != -1:
                    df.at[i, 'proper'] = True
    # # Manually annotate the improper responses to try to salvage something
    # for i, row in df[(df['proper'] == False) & (df['response'] != "n a")].iterrows():
    #     print(f"Question: {row['question']}")
    #     print(f"Options: {row['options']}")
    #     print(f"Current response: {row['response']}")
    #     new_response = input("Enter new response: ")
    #     df.at[i, 'response'] = new_response

    df.to_csv(os.path.join('zero_shot_results', file), index=False)
    