import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(": ")
            if len(parts) == 2:
                letter, count = parts
                data.append([letter, int(count)])
    return pd.DataFrame(data, columns=['Letter', 'Count'])

# Replace these paths with the paths to your exact and approximate count files
exact_files = {
    'swedish': './exact_counter/exact_pg2100.txt',
    'spanish': './exact_counter/exact_pg5881.txt',
    'greek': './exact_counter/exact_pg31802.txt',
    'portuguese': './exact_counter/exact_pg62383.txt',
    'english': './exact_counter/exact_pg26361.txt'
}

approx_files = {
    'swedish': './approx_counter/approx_pg2100.txt',
    'spanish': './approx_counter/approx_pg5881.txt',
    'greek': './approx_counter/approx_pg31802.txt',
    'portuguese': './approx_counter/approx_pg62383.txt',
    'english': './approx_counter/approx_pg26361.txt'
}

space_saving_files = {
    'swedish': './space_saving/space_saving_pg2100.txt',
    'spanish': './space_saving/space_saving_pg5881.txt',
    'greek': './space_saving/space_saving_pg31802.txt',
    'portuguese': './space_saving/space_saving_pg62383.txt',
    'english': './space_saving/space_saving_pg26361.txt'
}

# Reading the data
exact_counts = {lang: read_data(exact_files[lang]) for lang in exact_files}
approx_counts = {lang: read_data(approx_files[lang]) for lang in approx_files}
space_saving_counts = {lang: read_data(space_saving_files[lang]) for lang in space_saving_files}

# Creating plots for each language
for lang in exact_counts:
    plt.figure(figsize=(10, 6))
    plt.bar(exact_counts[lang]['Letter'], exact_counts[lang]['Count'], alpha=0.5, label='Exact')
    plt.bar(approx_counts[lang]['Letter'], approx_counts[lang]['Count'], alpha=0.5, label='Approximate')
    plt.xlabel('Letter')
    plt.ylabel('Count')
    plt.title(f'Letter Counts Comparison in {lang.title()} (Exact vs Approximate)')
    plt.legend()
    plt.show()

# Creating plots for each language
for lang in exact_counts:
    plt.figure(figsize=(10, 6))
    plt.bar(exact_counts[lang]['Letter'], exact_counts[lang]['Count'], alpha=0.5, label='Exact')
    plt.bar(space_saving_counts[lang]['Letter'], space_saving_counts[lang]['Count'], alpha=0.5, label='Space-Saving k=10')
    plt.xlabel('Letter')
    plt.ylabel('Count')
    plt.title(f'Letter Counts Comparison in {lang.title()} (Exact vs Space-Saving k=10)')
    plt.legend()
    plt.show()