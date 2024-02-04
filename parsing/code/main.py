import os
import json
import csv
import statistics
import re

def extract_numbers_with_min_digits(data, min_digits=3):
    """
    Extracts all numbers with a minimum number of digits from a nested JSON structure,
    capturing specific patterns including numbers with commas, decimals,
    and certain currency symbols (€). It ignores patterns followed by any currency symbol except €.
    """
    numbers = []

    if isinstance(data, dict):
        for value in data.values():
            numbers.extend(extract_numbers_with_min_digits(value, min_digits))

    elif isinstance(data, list):
        for item in data:
            numbers.extend(extract_numbers_with_min_digits(item, min_digits))

    elif isinstance(data, str):
        # Regex pattern to capture numbers with commas, decimals, and € currency symbol
        # Ignores patterns followed by any currency symbol except €
        pattern = r'\b\d+(?:,\d{3})*(?:\.\d+)?€?\b'
        found_numbers = re.findall(pattern, data)
        for num in found_numbers:
            # Cleaning the number format
            num_clean = num.replace(',', '').replace('.', '').replace('€', '')
            if len(num_clean) >= min_digits:
                numbers.append(int(num_clean))

    return numbers



def process_json_file(json_file_path, folder_name):
    """
    Process a single JSON file and return the extracted data for each person.
    Includes both the original and modified list of extracted numbers for each person.
    """
    with open(json_file_path, 'r') as json_file:
        conversation = json.load(json_file)
        persons_data = {}

        # Extract numbers for each person and maintain original and modified lists
        for message in conversation:
            name = message['name']
            content = message['content']
            if name not in persons_data:
                persons_data[name] = {'original': [], 'modified': []}

            content_numbers = extract_numbers_with_min_digits(content)
            persons_data[name]['original'].extend(content_numbers)

            # Modify the list by removing the first number if more than one
            modified_numbers = content_numbers[1:] if len(content_numbers) > 1 else content_numbers
            persons_data[name]['modified'].extend(modified_numbers)

        # Compile data for CSV
        csv_data = []
        for name, numbers in persons_data.items():
            original_numbers = numbers['original']
            modified_numbers = numbers['modified']

            min_price = min(modified_numbers) if modified_numbers else 0
            max_price = max(modified_numbers) if modified_numbers else 0
            avg_price = statistics.mean(modified_numbers) if modified_numbers else 0
            last_price = modified_numbers[-1] if modified_numbers else 0
            csv_data.append([25, name, min_price, max_price, avg_price, last_price, folder_name, original_numbers, modified_numbers])

        return csv_data

def write_to_csv(csv_file_path, csv_data):
    """
    Write data to a CSV file.
    """
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Apartment Size', 'Name', 'Min Price', 'Max Price', 'Avg Price', 'Last Price', 'Folder Name', 'Original Price List', 'Modified Price List'])
        for row in csv_data:
            # Convert the lists of prices to string representations for CSV writing
            row[-2] = ', '.join(map(str, row[-2]))  # Original Price List
            row[-1] = ', '.join(map(str, row[-1]))  # Modified Price List
            writer.writerow(row)

# Update the process_folder function to handle the new CSV data structure
def process_folder(base_path, output_directory):
    """
    Process each folder in 'single-factor-experiments' and create a single CSV file for each folder.
    Each CSV file contains data from all JSON files within the subfolders of that folder.
    """
    for renter_name in os.listdir(base_path):
        renter_path = os.path.join(base_path, renter_name)

        if os.path.isdir(renter_path):
            all_csv_data = []
            for json_folder in os.listdir(renter_path):
                json_folder_path = os.path.join(renter_path, json_folder)

                for file in os.listdir(json_folder_path):
                    if file.endswith('.json'):
                        json_file_path = os.path.join(json_folder_path, file)
                        csv_data = process_json_file(json_file_path, json_folder)
                        all_csv_data.extend(csv_data)

            # Write the data to a CSV file
            csv_file_name = f"{renter_name}.csv"
            csv_file_path = os.path.join(output_directory, csv_file_name)
            write_to_csv(csv_file_path, all_csv_data)

