import unicodedata
import nltk
import os
import re
import string
import sys
from nltk.corpus import stopwords

# List of avaiable content documents and their respective languages
file_langs = {
    './content/pg26361.txt':'english',
    './content/pg31802.txt':'greek',
    './content/pg2100.txt':'swedish',
    './content/pg5881.txt':'spanish',
    './content/pg62383.txt':'portuguese'
}

# Set NLTK data path and download stopwords
nltk.download('stopwords')

def normalize_text(text: str, lang: str = None):
    # Check if the language uses Latin alphabet and apply normalization
    if lang in ['english', 'spanish', 'portuguese', 'swedish']:
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    else:
        return text
    
# Function to preprocess text data using custom stopwords from a file
def preprocess_text(file_path: str, lang : str = None):
    
    print(f"Processing file {file_path}")
    
    # Obtain file languague
    if lang is None:
        if file_path not in file_langs.keys():
            print(f'File {file_path} is not registered in for the file languages.')
            exit(1)

    # Define file paths
    output_file_path = f'./processed/{file_path.replace("./content/","")}'

    # Regular expressions for start and end markers
    start_marker_regex = r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK .* \*\*\*"
    end_marker_regex = r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK .* \*\*\*"

    # Read the input file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Find start and end markers using regex
    start_index = re.search(start_marker_regex, text)
    end_index = re.search(end_marker_regex, text)

    # Extract text between start and end markers
    text = text[start_index.end():end_index.start()] if start_index and end_index else text

    # Convert to uppercase and remove extended punctuation
    text = text.upper()
    extended_punctuation = string.punctuation + "“”‘’-"
    text = text.translate(str.maketrans('', '', extended_punctuation))

    # Remove stopwords using NLTK
    lang_stopwords = set(stopwords.words(lang))
    text = ' '.join([word for word in text.split() if word not in lang_stopwords])

    # Removing digits and extra spaces
    text = re.sub(r'\d+', '', text).strip()
    text = text.replace('»', '').replace('«', '').replace(' ', '')
    
    # Normalize the text
    text = normalize_text(text, lang)

    # Save the preprocessed text to a new file
    if not os.path.exists('./processed'):
        os.makedirs('./processed')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

    print(f"Processed text saved to ./processed/ directory.")

# Manual usage
if __name__ == "__main__":
    
    # 'python process.py' 
    if len(sys.argv) == 1:
        for file in os.listdir('./content/'):
            if '.txt' in os.path.basename(file):
                preprocess_text(f'./content/{file}')

    # 'python process.py <file_path>'
    elif len(sys.argv) == 2:
        preprocess_text(sys.argv[1])

    # Wrong usage
    else:
        print("Usage:")
        print(" python process.py")
        print("OR")
        print(" python process.py <file_path>")
        sys.exit(1)

