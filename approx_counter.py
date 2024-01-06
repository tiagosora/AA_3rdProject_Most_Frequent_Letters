import random
from collections import Counter
import os
import sys

def approximate_count_fixed_probability(file_path: str, probability: float = 1/8):
    
    # Read the preprocessed file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

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
    output_file_path = f'./approx_counter/{file_path.replace("./processed/","")}'
    if not os.path.exists('./approx_counter'):
        os.makedirs('./approx_counter')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        sorted_approximate_counts = sorted(approximate_counts.items(), key=lambda x: x[1], reverse=True)
        for letter, count in sorted_approximate_counts:
            output_file.write(f"{letter}: {count}\n")
        print(f"Approximate counts saved to: {output_file_path}")
        
    return sorted_approximate_counts

# Manual usage
if __name__ == "__main__":
    
    # 'python approximate_counter.py <file_path>'
    if len(sys.argv) == 2:
        # User specified a single file to process
        approximate_count_fixed_probability(sys.argv[1])
    
    # 'python approximate_counter.py'
    elif len(sys.argv) == 1:
        # Process all files in the ./processed/ directory
        for file in os.listdir('./processed/'):
            if file.endswith('.txt'):
                approximate_count_fixed_probability(f'./processed/{file}')
    
    # Wrong usage
    else:
        print("Usage:")
        print(" python approximate_counter.py")
        print("OR")
        print(" python approximate_counter.py <file_path>")
        sys.exit(1)
