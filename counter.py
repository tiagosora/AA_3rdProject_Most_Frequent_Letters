import unicodedata
from collections import Counter
import os
import sys

def normalize_text(text, lang):
    # Check if the language uses Latin alphabet and apply normalization
    if lang in ['english', 'spanish', 'portuguese', 'swedish']:
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    else:
        return text

def count_letters_and_save(file_path, output_file_path, lang):
    # Read the preprocessed file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Normalize text if applicable
    text = normalize_text(text, lang)

    # Count occurrences of each letter
    letter_counts = Counter(filter(str.isalpha, text))

    # Save the letter counts to a file
    if not os.path.exists('./letter_counts'):
        os.makedirs('./letter_counts')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for letter, count in dict(sorted(letter_counts.items())).items():
            output_file.write(f"{letter}: {count}\n")

    return letter_counts

file_langs = {
    'pg26361':'english',
    'pg31802':'greek',
    'pg2100':'swedish',
    'pg5881':'spanish',
    'pg62383':'portuguese'
}

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # User specified a single file to process
        file_name = sys.argv[1]
        lang = file_langs[file_name]
        preprocessed_file_path = f'./processed/{file_name}.txt'
        output_file_path = f'./letter_counts/{file_name}.txt'
        result_file_path = count_letters_and_save(preprocessed_file_path, output_file_path, lang)
        print(f"Letter counts saved to: {output_file_path}")
    elif len(sys.argv) == 1:
        # Process all files in the ./processed/ directory
        for file in os.listdir('./processed/'):
            if file.endswith('.txt'):
                file_name = file[:-4]  # Remove .txt extension
                lang = file_langs[file_name]
                preprocessed_file_path = f'./processed/{file}'
                output_file_path = f'./letter_counts/{file_name}.txt'
                result_file_path = count_letters_and_save(preprocessed_file_path, output_file_path, lang)
                print(f"Letter counts saved to: {output_file_path}")
    else:
        print("Usage:")
        print(" python counter.py")
        print("OR")
        print(" python counter.py <file_name>")
        sys.exit(1)
