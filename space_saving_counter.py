import os
import sys
from typing import List

class SpaceSavingCounter:
    def __init__(self, k: int = 10):
        self.k = k
        self.counters = {}

    def process(self, file_path: str):
        # Read and process the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
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
        output_file_path = f'./space_saving/space_saving_{file_path.replace("./processed/","")}'
        if not os.path.exists('./space_saving'):
            os.makedirs('./space_saving')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            sorted_counters = sorted(self.counters.items(), key=lambda x: x[1], reverse=True)
            for letter, count in sorted_counters:
                output_file.write(f"{letter}: {count}\n")
                
        print(f"Top {self.k} frequent letters using Space-Saving algorithm saved to: {output_file_path}")
        
        return sorted_counters

# Manual usage
if __name__ == "__main__":
    
    # 'python space_saving_counter.py <file_name>'
    if len(sys.argv) == 2:
        # User specified a single file to process
        k = 10  # Number of top frequent items to find
        space_saving_counter = SpaceSavingCounter(k)
        space_saving_counter.process(sys.argv[1])
        
    # 'python space_saving_counter.py'
    elif len(sys.argv) == 1:
        # Process all files in the ./processed/ directory
        for file in os.listdir('./processed/'):
            if file.endswith('.txt'):
                k = 10  # Number of top frequent items to find
                space_saving_counter = SpaceSavingCounter(k)
                space_saving_counter.process(f'./processed/{file}')
    
    # Wrong usage
    else:
        print("Usage:")
        print(" python space_saving_counter.py")
        print("OR")
        print(" python space_saving_counter.py <file_name>")
        sys.exit(1)