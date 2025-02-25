import pandas as pd

# Read the CSV files
output_df = pd.read_csv('output.csv')
cover_df = pd.read_csv('cover_links.csv')

# Print column names to debug
print("Output CSV columns:", output_df.columns)
print("Cover links CSV columns:", cover_df.columns)

# Create new column in output_df
output_df['Cover File Link'] = ''

# Process cover_links.csv
for _, cover_row in cover_df.iterrows():
    try:
        show_name = cover_row['Show name'].lower()  # Convert to lowercase
        cover_link = cover_row['Upload your show graphic below']
        
        # Find matching rows in output_df using case-insensitive comparison
        mask = output_df['Show Name'].str.lower() == show_name
        output_df.loc[mask, 'Cover File Link'] = cover_link
        
    except Exception as e:
        print(f"Error processing row: {e}")

# Save updated DataFrame back to CSV
output_df.to_csv('output.csv', index=False)
