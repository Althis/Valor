import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('markets.csv')

# Since the classes are very unbalanced, we will be resolving any multicategory entries
# To their category with the most entries, then we will drop anything that has less than 20 examples
df['category'] = df['category'].apply(eval)
category_counts = df['category'].explode().value_counts()
df['category'] = df['category'].apply(lambda x: [i for i in x if category_counts[i] > 200] if len(x) > 1 else x)
df['category'] = df['category'].apply(lambda x: [max(x, key=category_counts.get)] if len(x) > 1 else x)
# Drop all rows with categories of under 20 members
df = df[df['category'].apply(lambda x: all(category_counts[i] > 20 for i in x))]

# Re-save it
df.to_csv('markets.csv', index=False)

pd.set_option('display.max_rows', None)
print(f"Total number of rows: {len(df)}")
print("\nClass distribution:")
print(df['category'].value_counts())
yes_no_count = df['options'].apply(lambda x: set(eval(x)) == {"Yes", "No"}).sum()
print(f"\nNumber of options that are just 'yes' and 'no': {yes_no_count}")
df['options_count'] = df['options'].apply(lambda x: len(eval(x)))
print("\nDistribution of rows per number of options:")
print(df['options_count'].value_counts())