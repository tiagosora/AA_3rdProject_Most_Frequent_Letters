import os
import sys
import unicodedata

class SpaceSavingCounter:
    def __init__(self, k, preprocessed_file_path):
        self.k = k
        self.preprocessed_file_path = preprocessed_file_path
        self.counters = {}

    def process(self, output_file_path):
        # Read and process the file
        with open(self.preprocessed_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        text = normalize_text(text, lang)
        filtered_text = filter(str.isalpha, text)
    
        for item in filtered_text:
            if item in self.counters:
                self.counters[item] += 1
            elif len(self.counters) < self.k:
                self.counters[item] = 1
            else:
                min_item = min(self.counters, key=self.counters.get)
                self.counters[item] = self.counters.pop(min_item) + 1
                
        # Save results to file
        if not os.path.exists('./space_saving'):
            os.makedirs('./space_saving')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for letter, count in self.get_top_k():
                output_file.write(f"{letter}: {count}\n")
                
        print(f"Top {k} frequent letters using Space-Saving algorithm saved to: {output_file_path}")

    def get_top_k(self):
        return sorted(self.counters.items(), key=lambda x: x[1], reverse=True)

def normalize_text(text, lang):
    if lang in ['english', 'spanish', 'portuguese', 'swedish']:
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    else:
        return text

file_langs = {
    'pg26361': 'english',
    'pg31802': 'greek',
    'pg2100': 'swedish',
    'pg5881': 'spanish',
    'pg62383': 'portuguese'
}

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # User specified a single file to process
        file_name = sys.argv[1]
        lang = file_langs[file_name]
        preprocessed_file_path = f'./processed/{file_name}.txt'
        output_file_path = f'./space_saving/{file_name}.txt'
        
        k = 10  # Number of top frequent items to find
        space_saving_counter = SpaceSavingCounter(k, preprocessed_file_path)
        space_saving_counter.process(output_file_path)
        
    elif len(sys.argv) == 1:
        # Process all files in the ./processed/ directory
        for file in os.listdir('./processed/'):
            if file.endswith('.txt'):
                file_name = file[:-4]  # Remove .txt extension
                lang = file_langs[file_name]
                preprocessed_file_path = f'./processed/{file}'
                output_file_path = f'./space_saving/{file_name}.txt'
                
                k = 10  # Number of top frequent items to find
                space_saving_counter = SpaceSavingCounter(k, preprocessed_file_path)
                space_saving_counter.process(output_file_path)
    else:
        print("Usage:")
        print(" python space_saving_counter.py")
        print("OR")
        print(" python space_saving_counter.py <file_name>")
        sys.exit(1)