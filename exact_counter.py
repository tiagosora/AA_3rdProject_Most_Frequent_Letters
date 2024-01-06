from collections import Counter
import os
import sys

def count_letters_and_save(file_path: str):
    
    # Read the preprocessed file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Count occurrences of each letter
    letter_counts = Counter(filter(str.isalpha, text))

    # Save the letter counts to a file
    output_file_path = f'./exact_counter/{file_path.replace("./processed/","")}'
    if not os.path.exists('./exact_counter'):
        os.makedirs('./exact_counter')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        sorted_letter_counts = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)
        for letter, count in sorted_letter_counts:
            output_file.write(f"{letter}: {count}\n")
        print(f"Letter counts saved to: {output_file_path}")
        
    return sorted_letter_counts

# Manual usage
if __name__ == "__main__":
    
    # 'python counter.py'
    if len(sys.argv) == 2:
        # User specified a single file to process
        count_letters_and_save(sys.argv[1])
    
    # 'python counter.py <file_path>'
    elif len(sys.argv) == 1:
        # Process all files in the ./processed/ directory
        for file in os.listdir('./processed/'):
            if file.endswith('.txt'):
                count_letters_and_save(f'./processed/{file}')
    
    # Wrong usage
    else:
        print("Usage:")
        print(" python counter.py")
        print("OR")
        print(" python counter.py <file_path>")
        sys.exit(1)
