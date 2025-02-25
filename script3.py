import csv
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Replace with your service account credentials file
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authenticate and build the service
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# Replace with the ID of your main folder (the one containing subfolders)
MAIN_FOLDER_ID = '165Sv10HAqncFKPF1BpS7u2UH059a28l4'

# CSV output file
CSV_FILENAME = 'audio_files.csv'

def get_subfolders(parent_folder_id):
    """Retrieves all subfolder IDs inside a given folder."""
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return [(folder['id'], folder['name']) for folder in results.get('files', [])]

def get_audio_files(folder_id):
    """Retrieves all audio files inside a given folder."""
    query = f"'{folder_id}' in parents and mimeType contains 'audio/'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return [(file['name'], f"https://drive.google.com/file/d/{file['id']}/view") for file in results.get('files', [])]

def save_to_csv(data):
    """Saves the collected audio file names and links to a CSV file."""
    with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Audio File Name", "Audio File Link"])  # Header row
        writer.writerows(data)

def main():
    all_audio_files = []
    
    # Get all subfolders inside the main folder
    subfolders = get_subfolders(MAIN_FOLDER_ID)
    
    for folder_id, folder_name in subfolders:
        print(f"Scanning folder: {folder_name}...")
        audio_files = get_audio_files(folder_id)
        all_audio_files.extend(audio_files)

    # Save results to CSV
    save_to_csv(all_audio_files)
    print(f"Audio file data saved to {CSV_FILENAME}")

# Add this line to execute the main function when the script runs
if __name__ == "__main__":
    main()

main()