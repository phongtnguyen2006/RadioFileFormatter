import pandas as pd

# Read the CSV file
df = pd.read_csv('input.csv')

# Split 'Subject' column into show name and DJs
df[['Show Name', 'temp']] = df['Subject'].str.split(',', n=1, expand=True)

# Process DJs
def extract_djs(dj_string):
    if pd.isna(dj_string):
        return ['N/A', 'N/A', 'N/A']
    
    djs = ['N/A', 'N/A', 'N/A']
    dj_count = 0
    
    # Split by both 'and' and ','
    parts = dj_string.replace(' and ', ',').split(',')
    
    # If no "DJ" in the string, capture first part after comma
    if 'DJ' not in dj_string and len(parts) > 0:
        djs[0] = parts[0].strip()
        return djs
    
    # Otherwise process DJs as before
    for part in parts:
        part = part.strip()
        if 'DJ' in part and dj_count < 3:
            dj_name = part[part.find('DJ'):].strip()
            djs[dj_count] = dj_name
            dj_count += 1
            
    return djs

# Create DJ columns
dj_columns = df['temp'].apply(extract_djs).apply(pd.Series)
dj_columns.columns = ['DJ1', 'DJ2', 'DJ3']

# Add DJ columns to dataframe
df = pd.concat([df, dj_columns], axis=1)

# Drop original Subject and temp columns
df.drop(['Subject', 'temp'], axis=1, inplace=True)

# Reorder columns to put Show Name and DJs first
column_order = ['Show Name', 'DJ1', 'DJ2', 'DJ3'] + [col for col in df.columns if col not in ['Show Name', 'DJ1', 'DJ2', 'DJ3']]
df = df[column_order]

# Convert 'Start Date' column from mm/dd/yyyy to yyyy-mm-dd
df['Start Date'] = pd.to_datetime(df['Start Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

# Convert 'Time' column to 24-hour format and extract hour
df['Hour'] = pd.to_datetime(df['Start Time'], format='%I:%M %p').dt.hour

# Combine date and hour to create Date-Time column
df['Date-Time'] = df['Start Date'] + '-' + df['Hour'].astype(str).str.zfill(2)

# Drop the temporary Hour column
df.drop('Hour', axis=1, inplace=True)

# Save the modified DataFrame back to CSV
df.to_csv('output.csv', index=False)