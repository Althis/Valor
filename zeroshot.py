import ollama
from tqdm import tqdm
import os
import pandas as pd

# We will primarily use the txt prompts, but markets still has valuable info
markets_df = pd.read_csv('markets.csv')

# Define the input files and corresponding models
input_files = {
    'simplequestions.txt': [ 'llama2form1', 'llama2form2', 'llama2textform1', 'llama2textform2', 'mistralform1', 'mistralform2', 'mistralinstructform1', 'mistralinstructform2', 'llama2form5', 'llama2form6', 'llama2textform5', 'llama2textform6'],
    'taggedsimplequestions.txt': ['llama2form3', 'llama2form4', 'llama2textform3', 'llama2textform4', 'mistralform3', 'mistralform4', 'mistralinstructform3', 'mistralinstructform4', 'llama2form7', 'llama2form8', 'llama2textform7', 'llama2textform8'],
    'extendedquestions.txt': [ 'llama2form1', 'llama2form2', 'llama2textform1', 'llama2textform2', 'mistralform1', 'mistralform2', 'mistralinstructform1', 'mistralinstructform2', 'llama2form5', 'llama2form6', 'llama2textform5', 'llama2textform6'],
    'taggedextendedquestions.txt': ['llama2form3', 'llama2form4', 'llama2textform3', 'llama2textform4', 'mistralform3', 'mistralform4', 'mistralinstructform3', 'mistralinstructform4', 'llama2form7', 'llama2form8', 'llama2textform7', 'llama2textform8'],
}

for input_file, model_names in input_files.items():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for model_name in model_names:
        print(f"Processing {input_file} with {model_name}")
        output = []
        # We will be reducing our analysis to just the first 100 lines
        # As otherwise, this task will not finish.
        for line in tqdm(lines[:100]):
            response = ollama.generate(model=model_name, prompt=line)
            respose = response['response'].replace('\n', '').replace('\r', '') 
            output.append({'response': response['response'], 'full_response': response})

        output_df = pd.DataFrame(output)

        merged_df = pd.concat([markets_df, output_df], axis=1)

        output_file = f"{input_file}-output-{model_name}.csv"
        merged_df.to_csv(output_file, index=False)

# Second pass for fewshot
# Same thing, but with the added "f" that defines fewshot models
for input_file, model_names in input_files.items():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for model_name in model_names:
        model_name = f"{model_name}f"
        print(f"Processing {input_file} with {model_name}")
        output = []
        for line in tqdm(lines[:100]):
            response = ollama.generate(model=model_name, prompt=line)
            respose = response['response'].replace('\n', '').replace('\r', '')  
            output.append({'response': response['response'], 'full_response': response})

        output_df = pd.DataFrame(output)

        merged_df = pd.concat([markets_df, output_df], axis=1)

        output_file = f"{input_file}-output-{model_name}.csv"
        merged_df.to_csv(output_file, index=False)