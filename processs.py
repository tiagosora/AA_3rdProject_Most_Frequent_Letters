import nltk
import os
import re
import string
import sys
from nltk.corpus import stopwords

file_langs = {
    'pg26361':'english',
    'pg31802':'greek',
    'pg2100':'swedish',
    'pg5881':'spanish',
    'pg62383':'portuguese'
}

# Function to preprocess text data using custom stopwords from a file
def preprocess_text(file_name, lang):

    # Define file paths
    input_file_path = f'./content/{file_name}.txt'
    output_file_path = f'./processed/{file_name}.txt'

    # Regular expressions for start and end markers
    start_marker_regex = r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK .* \*\*\*"
    end_marker_regex = r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK .* \*\*\*"

    # Read the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
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
    text = re.sub(r'\d+ ', '', text).strip()

    # Save the preprocessed text to a new file
    if not os.path.exists('./processed'):
        os.makedirs('./processed')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

    return output_file_path

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Set NLTK data path and download stopwords
        nltk.download('stopwords')

        for file in os.listdir('./content/'):
            if '.txt' in os.path.basename(file):
                
                print(f"\nProcessing file {file}")
                
                file_name = file[:-4]                                       # Remove .txt
                lang = file_langs[file_name]
                preprocessed_file_path = preprocess_text(file_name, lang)
                
                print(f"Processed text saved to: {preprocessed_file_path}")
                
    elif len(sys.argv) == 3:
        # Set NLTK data path and download stopwords
        nltk.download('stopwords')
        
        file_name = sys.argv[1]
        lang = sys.argv[2]
        preprocessed_file_path = preprocess_text(file_name, lang)
        
        print(f"Processed text saved to: {preprocessed_file_path}")
        
    else:
        print("Usage:")
        print(" python preprocess.py")
        print("OR")
        print(" python preprocess.py <file_name> <language>")
        sys.exit(1)

