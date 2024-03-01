import os
import csv
import datetime
from bibtexparser.bparser import BibTexParser
from slugify import slugify

def parse_bibtex(bibtex_path):
    with open(bibtex_path, 'r', encoding='utf-8') as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.ignore_nonstandard_types = False
        bibtex_data = bibtex_file.read()
        bibtex_db = parser.parse(bibtex_data)
        return bibtex_db.entries

def merge_bibtex_to_csv(folder_path):
    merged_data = []
    fieldnames = [
                'BibtexKey', 'Title', 'Abstract', 'Author', 'Journal', 'BookTitle', 'Year',
                'Doi', 'Url', 'Source', 'CreatedAt', 'Status'
            ]
    
    total = 0
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".bib"):
            count = 0
            bibtex_path = os.path.join(folder_path, filename)
            entries = parse_bibtex(bibtex_path)
            for entry in entries:
                merged_entry = {
                    'BibtexKey': entry.get('ID', ''),
                    'Title': entry.get('title', ''),
                    'Abstract': entry.get('abstract', ''),
                    'Author': entry.get('author', ''),
                    'Journal': entry.get('journal', ''),
                    'BookTitle': entry.get('booktitle', ''),
                    'Year': entry.get('year', ''),
                    'Doi': entry.get('doi', ''),
                    'Url': entry.get('url', ''),
                    'Source': filename,
                    'CreatedAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Status': 'Unclassified'

                }
                merged_data.append(merged_entry)
                count += 1
            total += count
            print("* Read " + str(count) + " entries from " + filename)
    print("** Read " + str(total) + " entries in total")
    
    # Merge duplicates based on slugified title similarity
    unique_entries = []
    duplicate_entries = []
    seen_titles = set()

    for entry in merged_data:
        title_slug = slugify(entry['Title'])
        if title_slug in seen_titles:
            duplicate_entries.append(entry)
        else:
            seen_titles.add(title_slug)
            unique_entries.append(entry)
    
    print("- Saved " + str(len(duplicate_entries)) + " duplicated entries and " + str(len(unique_entries)) + " unique entries.")
    print()

    # Write merged data to a CSV file with specified fieldnames
    if unique_entries:
        with open('merged_bibtex.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_entries)
    
    # Write duplicates to a CSV file with specified fieldnames
    if duplicate_entries:
        with open('duplicate_bibtex.csv', 'w', newline='', encoding='utf-8') as dup_file:
            writer = csv.DictWriter(dup_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(duplicate_entries)


def compare_and_save_unique_entries(file1_path, file2_path):
    unique_titles = set()
    unique_entries = []

    with open(file1_path, 'r', newline='') as file1:
        reader1 = csv.DictReader(file1)
        for row in reader1:
            title = slugify(row['Title'])
            unique_titles.add(title)

    with open(file2_path, 'r', newline='') as file2:
        reader2 = csv.DictReader(file2)
        for row in reader2:
            title = slugify(row['Title'])
            if title not in unique_titles:
                unique_entries.append(row)

    print("* Found " + str(len(unique_entries)) + " unique entries.")

    fieldnames = reader2.fieldnames  # Assuming both files have the same structure
    with open('merged_csv.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_entries)

def main():
    while True:
        print("1. Merge Bibtex files to CSV")
        print("2. Compare two CSV files")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            folder_path = input("Enter the folder path containing Bibtex files: ")
            merge_bibtex_to_csv(folder_path)
            print("CSV file generated.")
        elif choice == '2':
            csv1_path = input("Enter the path of the first CSV file: ")
            csv2_path = input("Enter the path of the second CSV file: ")
            compare_and_save_unique_entries(csv1_path, csv2_path)
            print("Comparison completed. Unique entries CSV generated.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
