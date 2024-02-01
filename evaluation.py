import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.metrics import cohen_kappa_score
import re
import numpy as np

def process_csv(file):
    df = pd.read_csv(file)
    df = df.fillna("N A")
    df['response'] = df['response'].astype(str)
    df['outcome'] = df['outcome'].astype(str)
    df['match'] = df.apply(lambda row: row['outcome'].lower() in row['response'].lower(), axis=1)
    df['proper'] = df['proper'].astype(bool)  # ensure 'proper' is a boolean
    df['proper_hits'] = df.apply(lambda row: row['match'] and row['proper'], axis=1)
    return df  # return the entire DataFrame

results = {}
directory = 'zero_shot_results'
for file in os.listdir(directory):
    if file.endswith('.csv'):
        df = process_csv(os.path.join(directory, file))
        match_result = df['match'].value_counts()
        proper_hits_result = df['proper_hits'].value_counts()
        hit = match_result.get(True, 0)
        proper_hit = proper_hits_result.get(True, 0)
        results[file] = (hit, proper_hit)

# Sort results by 'hits' and select top 10
sorted_results = sorted(results.items(), key=lambda x: x[1][0], reverse=True)[:20]

labels = [x[0].replace('.txt', ' ').replace('.csv', ' ').replace('form', ' ').replace('-output-', ' ').replace('questions', '') for x in sorted_results]
hits = [x[1][0] for x in sorted_results]
mistakes = [x[1][1] for x in sorted_results]

x = np.arange(len(labels))

width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, hits, width, label='Hit')
rects2 = ax.bar(x + width/2, mistakes, width, label='Proper-Hit')

ax.set_ylabel('Counts')
ax.set_title('Hits and Proper-Hits by file')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation='vertical')  # rotate labels
ax.set_ylim([0, 10]) 
ax.set_yticks(range(11))
ax.legend()

fig.tight_layout()
plt.subplots_adjust(bottom=0.5)  # adjust bottom margin

plt.show()


category_hits = {}
category_counts = {}

for file in os.listdir(directory):
    if file.endswith('.csv'):
        df = process_csv(os.path.join(directory, file))
        for category in df['category'].unique():
            if category not in category_hits:
                category_hits[category] = df[df['category'] == category]['match'].sum()
                category_counts[category] = df[df['category'] == category].shape[0]
            else:
                category_hits[category] += df[df['category'] == category]['match'].sum()
                category_counts[category] += df[df['category'] == category].shape[0]

category_hit_rate = {category: hits / category_counts[category] for category, hits in category_hits.items()}
sorted_category_hit_rate = sorted(category_hit_rate.items(), key=lambda x: x[1], reverse=True)

plt.figure(figsize=(10, 5))
plt.bar(*zip(*sorted_category_hit_rate))
plt.xlabel('Category')
plt.ylabel('Hit Rate')
plt.title('Hit Rate per Category')
plt.xticks(rotation='vertical')  # rotate x-axis labels
plt.tight_layout()
plt.show()

model_family_yes_counts = {}
model_family_total_counts = {}
model_families = ['llama2form', 'llama2textform', 'mistralform', 'mistralinstructform']
for model_family in model_families:
    dfs = []
    for file in os.listdir(directory):
        if model_family in file and file.endswith('.csv'):
            df = process_csv(os.path.join(directory, file))
            dfs.append(df)
    merged_df = pd.concat(dfs)
    yes_no_df = merged_df[merged_df['response'].isin(['yes', 'no'])] 
    if model_family not in model_family_yes_counts:
        model_family_yes_counts[model_family] = yes_no_df[yes_no_df['response'] == 'yes'].shape[0]
        model_family_total_counts[model_family] = yes_no_df.shape[0]
    else:
        model_family_yes_counts[model_family] += yes_no_df[yes_no_df['response'] == 'yes'].shape[0]
        model_family_total_counts[model_family] += yes_no_df.shape[0]

model_family_yes_rate = {model_family: (yes_counts / model_family_total_counts[model_family]) if model_family_total_counts[model_family] != 0 else 0 for model_family, yes_counts in model_family_yes_counts.items()}
sorted_model_family_yes_rate = sorted(model_family_yes_rate.items(), key=lambda x: x[1], reverse=True)

plt.figure(figsize=(10, 5))
plt.bar(*zip(*sorted_model_family_yes_rate))
plt.xlabel('Model Family')
plt.ylabel('"Yes" Response Rate')
plt.title('"Yes" Response Rate per Model Family for "Yes" or "No" Outcomes')
plt.xticks(rotation='vertical')  # rotate x-axis labels
plt.tight_layout()
plt.show()

def is_even(filename):
    number = re.findall(r'\d+', filename)
    if number:
        return int(number[-1]) % 2 == 0
    return False

even_results = {}
odd_results = {}

for file in os.listdir(directory):
    if file.endswith('.csv'):
        df = process_csv(os.path.join(directory, file))
        match_result = df['match'].value_counts()
        hit = match_result.get(True, 0)
        total = match_result.sum()
        if is_even(file):
            even_results[file] = (hit, total)
        else:
            odd_results[file] = (hit, total)

even_accuracy = sum(hit for hit, total in even_results.values()) / sum(total for hit, total in even_results.values())
odd_accuracy = sum(hit for hit, total in odd_results.values()) / sum(total for hit, total in odd_results.values())

plt.bar(['Predict', 'Guess'], [even_accuracy, odd_accuracy])
plt.ylabel('Accuracy')
plt.title('Accuracy of Predict and Guess Models')
plt.show()

def is_tagged(filename):
    return 'tagged' in filename

tagged_results = {}
untagged_results = {}

for file in os.listdir(directory):
    if file.endswith('.csv'):
        df = process_csv(os.path.join(directory, file))
        match_result = df['match'].value_counts()
        hit = match_result.get(True, 0)
        total = match_result.sum()
        if is_tagged(file):
            tagged_results[file] = (hit, total)
        else:
            untagged_results[file] = (hit, total)

tagged_accuracy = sum(hit for hit, total in tagged_results.values()) / sum(total for hit, total in tagged_results.values())
untagged_accuracy = sum(hit for hit, total in untagged_results.values()) / sum(total for hit, total in untagged_results.values())

plt.bar(['Tagged', 'Untagged'], [tagged_accuracy, untagged_accuracy])
plt.ylabel('Accuracy')
plt.title('Accuracy of Tagged and Untagged Models')
plt.show()

def is_extended(filename):
    return 'extended' in filename

extended_results = {}
simple_results = {}

for file in os.listdir(directory):
    if file.endswith('.csv'):
        df = process_csv(os.path.join(directory, file))
        match_result = df['match'].value_counts()
        hit = match_result.get(True, 0)
        total = match_result.sum()
        if is_extended(file):
            extended_results[file] = (hit, total)
        else:
            simple_results[file] = (hit, total)

extended_accuracy = sum(hit for hit, total in extended_results.values()) / sum(total for hit, total in extended_results.values())
simple_accuracy = sum(hit for hit, total in simple_results.values()) / sum(total for hit, total in simple_results.values())

plt.bar(['Extended', 'Simple'], [extended_accuracy, simple_accuracy])
plt.ylabel('Accuracy')
plt.title('Accuracy of Extended and Simple prompts')
plt.show()

def is_llama2(filename):
    return 'llama2' in filename

def ends_with_1_to_4(filename):
    number = re.findall(r'\d+', filename)
    if number:
        return 1 <= int(number[-1]) <= 4
    return False

def ends_with_5_to_8(filename):
    number = re.findall(r'\d+', filename)
    if number:
        return 5 <= int(number[-1]) <= 8
    return False

one_to_four_results = {}
five_to_eight_results = {}

for file in os.listdir(directory):
    if file.endswith('.csv') and is_llama2(file):
        df = process_csv(os.path.join(directory, file))
        match_result = df['match'].value_counts()
        hit = match_result.get(True, 0)
        total = match_result.sum()
        if ends_with_1_to_4(file):
            one_to_four_results[file] = (hit, total)
        elif ends_with_5_to_8(file):
            five_to_eight_results[file] = (hit, total)

one_to_four_accuracy = sum(hit for hit, total in one_to_four_results.values()) / sum(total for hit, total in one_to_four_results.values())
five_to_eight_accuracy = sum(hit for hit, total in five_to_eight_results.values()) / sum(total for hit, total in five_to_eight_results.values())

plt.bar(["Unconstrained", "Constrained"], [one_to_four_accuracy, five_to_eight_accuracy])
plt.ylabel('Average Accuracy')
plt.title('Were we able to constrain Llama2?')
plt.show()