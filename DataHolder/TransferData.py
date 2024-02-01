import os

directory = 'AquascopeData'  # Replace with the directory path containing your CSV files
output_file = 'AquascopeDataFileNames.csv'  # Name of the output text file

csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]

with open(output_file, 'w') as file:
    file.write(','.join(csv_files))
