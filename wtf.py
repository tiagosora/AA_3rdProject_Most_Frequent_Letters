from collections import Counter

def find_top_frequent_letters(file_path, n):
    # Read the preprocessed file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Count occurrences of each letter
    letter_counts = Counter(filter(str.isalpha, text))

    # Find the n most common letters
    top_n_letters = letter_counts.most_common(n)

    return top_n_letters

# Example usage
content = 'beyone_good_and_evil_english'
preprocessed_file_path = f'./processed/{content}.txt'

# Find top 3, 5, and 10 frequent letters
top_3_letters = find_top_frequent_letters(preprocessed_file_path, 3)
top_5_letters = find_top_frequent_letters(preprocessed_file_path, 5)
top_10_letters = find_top_frequent_letters(preprocessed_file_path, 10)

print("Top 3 frequent letters:", top_3_letters)
print("Top 5 frequent letters:", top_5_letters)
print("Top 10 frequent letters:", top_10_letters)
