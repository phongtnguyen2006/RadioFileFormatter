import csv

def convert_to_stream_link(download_link):
    """Convert download link to streaming link"""
    try:
        # Extract file ID from the download link
        # Format changes from "https://drive.google.com/uc?id=FILE_ID" to
        # "https://drive.google.com/file/d/FILE_ID/preview"
        file_id = download_link.split('id=')[1]
        return f"https://drive.google.com/file/d/{file_id}/preview"
    except:
        return download_link

def run():
    # Read audio files and their links into a dictionary
    audio_links = {}
    print("Reading audio_files.csv...")
    try:
        with open('audio_files.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                filename = row['Audio File Name'].replace('.mp3', '')  # Remove .mp3 extension
                # Convert download link to streaming link
                stream_link = convert_to_stream_link(row['Audio File Link'])
                audio_links[filename] = stream_link
    except FileNotFoundError:
        print("Error: audio_files.csv not found!")
        return

    # Process output.csv
    rows_to_write = []
    print("Processing output.csv...")
    try:
        with open('output.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            headers = list(reader.fieldnames) + ['file-link']
            
            for row in reader:
                # Use the Date-Time column directly
                key = row['Date-Time']
                # Add link if match found
                row['file-link'] = audio_links.get(key, '')
                if row['file-link']:
                    print(f"Match found for {key}")
                rows_to_write.append(row)

        # Write updated data back to output.csv
        print(f"Writing {len(rows_to_write)} rows back to output.csv...")
        with open('output.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows_to_write)
        print("Done!")

    except FileNotFoundError:
        print("Error: output.csv not found!")
        return

run()
