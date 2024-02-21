import pandas as pd
import ast
import os
import re
import csv


# Get all the csv files in the directory
result_files = [f for f in os.listdir('zero_shot_results') if f.endswith('.csv')]
pd.set_option('display.max_rows', None)

for file in result_files:
    df = pd.read_csv(os.path.join('zero_shot_results', file))
    print(file)
    df['question'] = df['question'].apply(lambda x: re.sub(r'\W|\n', ' ', str(x)).lower())
    df['description'] = df['description'].apply(lambda x: re.sub(r'\W|\n', ' ', str(x)).lower())
    df['options'] = df['options'].apply(lambda x: x.lower())
    df = df.iloc[:100]
    df['proper'] = False
    df = df.fillna("n a")

    # Remove newline, punctuation and special characters, convert to lowercase
    df['response'] = df['response'].apply(lambda x: re.sub(r'\W|\n', ' ', str(x)).lower())

    for i, row in df.iterrows():
        response = row['response']
        options = ast.literal_eval(row['options'])

        for option in options:
            if response.startswith('outcome ' + option):
                df.at[i, 'proper'] = True
                df.at[i, 'response'] = "outcome " + option
            else:
                # For improper rows we still search the options and replace with a proper response
                if options[0] in response and options[1] not in response:
                    df.at[i, 'response'] = "outcome " + options[0]
                elif options[1] in response and options[0] not in response:
                    df.at[i, 'response'] = "outcome " + options[1]
                else:
                    df.at[i, 'response'] = "n a"


    df.to_csv(os.path.join('zero_shot_results', file), index=False)
    