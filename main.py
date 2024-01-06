import os
import time
import tracemalloc
import json
from approx_counter import approximate_count_fixed_probability
from exact_counter import count_letters_and_save
from process_text import preprocess_text
from space_saving_counter import SpaceSavingCounter

def calculate_error(exact: dict, estimated: dict):
    absolute_error = {letter: abs(exact.get(letter, 0) - estimated.get(letter, 0)) for letter in set(exact) | set(estimated)}
    total_exact = sum(exact.values())
    relative_error = {letter: (error / total_exact) if total_exact else 0 for letter, error in absolute_error.items()}
    average_absolute_error = sum(absolute_error.values()) / len(absolute_error)
    average_relative_error = sum(relative_error.values()) / len(relative_error)
    return absolute_error, relative_error, average_absolute_error, average_relative_error

def store_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    
    # Preprocessing the text contents and save them to ./process/ directory
    for file in os.listdir('./content/'):
        if '.txt' in os.path.basename(file):
            preprocess_text(f'./content/{file}')

    data_exact = {}
    data_approx = {}
    data_ss = {}
    approx_runs = 50

    # Start measuring time and memory
    tracemalloc.start()
    start_time = time.time()

    # Process all files in the ./processed/ directory for exact and approximate counters
    for file in os.listdir('./processed/'):
        if file.endswith('.txt'):
            exact_counts = count_letters_and_save(f'./processed/{file}')
            data_exact[file] = {letter: count for letter, count in exact_counts}
            for i in range(approx_runs):
                approx_counts = approximate_count_fixed_probability(f'./processed/{file}')
                data_approx[(file, i)] = {letter: count for letter, count in approx_counts}

    # Process files for space-saving counter
    for k in [3, 5, 10]:
        for file in os.listdir('./processed/'):
            if file.endswith('.txt'):
                space_saving_counter = SpaceSavingCounter(k)
                space_saving_results = space_saving_counter.process(f'./processed/{file}')
                data_ss[(file, k)] = {letter: count for letter, count in space_saving_results}

    # Stop measuring time and memory
    end_time = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    performance_data = {
        'time': end_time - start_time,
        'memory': peak / 10**6
    }

    error_data = {}

    # Compute errors and compare results
    for file in data_exact:
        exact = data_exact[file]
        error_data[file] = {'approx': {}, 'space_saving': {}}

        for i in range(approx_runs):
            approx = data_approx[(file, i)]
            _, _, avg_abs_err, avg_rel_err = calculate_error(exact, approx)
            error_data[file]['approx'][f'run_{i}'] = {'avg_abs_error': avg_abs_err, 'avg_rel_error': avg_rel_err}

        for k in [3, 5, 10]:
            space_saving = data_ss[(file, k)]
            _, _, avg_abs_err, avg_rel_err = calculate_error(exact, space_saving)
            error_data[file]['space_saving'][f'k_{k}'] = {'avg_abs_error': avg_abs_err, 'avg_rel_error': avg_rel_err}

    # Store data for analysis
    store_data('performance_data.json', performance_data)
    store_data('error_data.json', error_data)

if __name__ == "__main__":
    main()
