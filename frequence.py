import pandas as pd
from difflib import SequenceMatcher

# Creating the function to count the protein names
# Here, the code considers that words with 70% similarity are the same word

def count_similar_names(file_path, sheet_name, column_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    names = df[column_name].tolist()

    name_counts = {}

    for i in range(len(names)):
        current_name = names[i]
        count = 1

        for j in range(i+1, len(names)):
            comparison_name = names[j]

            similarity = SequenceMatcher(None, current_name, comparison_name).ratio()
            similarity_threshold = 0.7

            if similarity >= similarity_threshold:
                count += 1

        name_counts[current_name] = count

    return name_counts

# Indicating the file with the data to be worked on
inp1 = input("File name: ")
inp2 = input("Sheet name: ")
inp3 = input("Column name: ")
inp4 = input ("Output name: ")
file_path = f"{inp1}.xlsx"
sheet_name = inp2
column_name = inp3

name_counts = count_similar_names(file_path, sheet_name, column_name)

for name, count in name_counts.items():
    print(f"{name}: {count}")

# Saving the results in another file
result = pd.DataFrame(list(name_counts.items()), columns=['Protein name', 'Count'])
result.to_excel(f"{inp4}.xlsx", index=False)