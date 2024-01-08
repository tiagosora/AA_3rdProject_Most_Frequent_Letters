import json
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def prepare_error_data(file_name, error_data, method_key):
    plot_data = {'File': [], 'Absolute Error': [], 'Relative Error': []}
    for file, errors in error_data.items():
        if file == file_name:
            if method_key in errors:
                for k, values in errors[method_key].items():
                    plot_data['File'].append(file)
                    plot_data['Absolute Error'].append(values['avg_abs_error'])
                    plot_data['Relative Error'].append(values['avg_rel_error'])
    return pd.DataFrame(plot_data)

def plot_errors(df, title, ylabel, column, method_key, file_name):
    
    file_langs = {
        'pg26361.txt':'English',
        'pg5881.txt':'Spanish',
        'pg31802.txt':'Greek',
        'pg62383.txt':'Portuguese',
        'pg2100.txt':'Swedish'
    }
    
    ax = df.plot(y=column, kind='bar', color='skyblue', figsize=(10, 6))
    
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(file_langs[file_name])
    plt.xticks([])

    # For the approximate counter, draw the average line
    if method_key == 'approx':
        avg_value = df[column].mean()
        ax.axhline(y=avg_value, color='red', linestyle='--', label=f'Average {column}')
        plt.legend()

    plt.show()

def main():
    # Load error data
    error_data = load_data('error_data.json')

    # Plot for each method
    for file_name in error_data:
        methods = {'approx': "Approximate Counter", 'space_saving': "Space-Saving Counter"}
        for method_key in methods.keys():
            df = prepare_error_data(file_name, error_data, method_key)
            plot_errors(df, f'Absolute Error - {methods[method_key]}', 'Error', 'Absolute Error', method_key, file_name)
            plot_errors(df, f'Relative Error - {methods[method_key]}', 'Error', 'Relative Error', method_key, file_name)

if __name__ == "__main__":
    main()
