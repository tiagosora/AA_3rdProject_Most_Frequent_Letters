import random
from collections import Counter
import os
import sys
import unicodedata

file_langs = {
    'pg26361': 'english',
    'pg31802': 'greek',
    'pg2100': 'swedish',
    'pg5881': 'spanish',
    'pg62383': 'portuguese'
}

def normalize_text(text, lang):
    if lang in ['english', 'spanish', 'portuguese', 'swedish']:
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    else:
        return text

def approximate_count_fixed_probability(file_path, lang, output_file_path, probability=1/8):
    # Read the preprocessed file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Normalize text if applicable
    text = normalize_text(text, lang)

    # Initialize an empty Counter
    approximate_counts = Counter()

    # Iterate over each letter and count with a fixed probability
    for letter in filter(str.isalpha, text):
        if random.random() < probability:
            approximate_counts[letter] += 1

    # Adjust the counts to estimate the total counts
    for letter in approximate_counts:
        approximate_counts[letter] *= int(1 / probability)
        
    # Save the results
    if not os.path.exists('./approx_counter'):
        os.makedirs('./approx_counter')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for letter, count in dict(sorted(approximate_counts.items())).items():
            output_file.write(f"{letter}: {count}\n")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # User specified a single file to process
        file_name = sys.argv[1]
        lang = file_langs[file_name]
        preprocessed_file_path = f'./processed/{file_name}.txt'
        output_file_path = f'./approx_counter/{file_name}.txt'
        approximate_count_fixed_probability(preprocessed_file_path, lang, output_file_path)
        print(f"Approximate counts saved to: {output_file_path}")
    elif len(sys.argv) == 1:
        # Process all files in the ./processed/ directory
        for file in os.listdir('./processed/'):
            if file.endswith('.txt'):
                file_name = file[:-4]  # Remove .txt extension
                lang = file_langs[file_name]
                preprocessed_file_path = f'./processed/{file}'
                output_file_path = f'./approx_counter/{file_name}.txt'
                approximate_count_fixed_probability(preprocessed_file_path, lang, output_file_path)
                print(f"Approximate counts saved to: {output_file_path}")
    else:
        print("Usage:")
        print(" python approximate_counter.py")
        print("OR")
        print(" python approximate_counter.py <file_name>")
        sys.exit(1)
