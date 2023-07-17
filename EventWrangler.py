import pandas as pd

# Prompt the user for the filename and provide format instructions
print("ATTENTION: This python script only processes soccer event data that has been uniquely defined by its writer!")
print("This script requires Python and Pandas to be installed for it to work.")
print("Please provide the Events CSV filename:")
print("- The filename can have spaces, hyphens, or underscores. Eg, player-events_file 1")
print("- Do not include the filename extension '.csv'.")

filename = input("Enter the CSV filename: ") + '.csv'

# Load data from the specified filename
df = pd.read_csv(filename)

# Prompt the user for tournament name, opponent team name, and match date
tournament_name = input("Enter the tournament name: ")
opponent_name = input("Enter the opponent team name: ")
match_date_str = input("Enter the match date (format: dd/mm/yyyy): ")

# Add Tournament and Opponent columns with user-provided values
df['Tournament'] = tournament_name
df['Opponent'] = opponent_name

# Convert the user-provided match date from string to datetime
match_date = pd.to_datetime(match_date_str, format="%d/%m/%Y")
df['Date'] = match_date

##Add Period markers
# Find the index of the row with 'HT' in the 'Event' column
ht_index = df[df['Event'] == 'HT'].index[0]
# Create the 'period' column and set all values to 'H2' by default
df['period'] = 'H2'
# Update values in 'period' column before and including 'HT' row to 'H1'
df.loc[:ht_index, 'period'] = 'H1'

##Create Video Timestamp
# Custom function to convert minutes and seconds to HH:MM:SS format
def format_time(row):
    hours = row['Mins'] // 60
    minutes = row['Mins'] % 60
    seconds = row['Secs']
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Apply the custom function to create the 'Timestamp' column
df['Timestamp'] = df.apply(format_time, axis=1)

#Split Event Column(Category, Event, Result)
split_values = df['Event'].str.split('-', expand=True)
# Assign new column names based on the split parts
split_values.columns = ['Category', 'Subcategory', 'Result']
# Update the original DataFrame by concatenating the split values
df = pd.concat([df, split_values], axis=1)

#Clean Category Column
clean_category = {
    'Def': 'Defense',
    'Off': 'Offense'
}

df['Category'] = df['Category'].replace(clean_category)

#Clean SubCategory Column
clean_sc = {
    'Gr': 'Ground',
    'Off': 'Off Target',
    'On': 'On Target',
    'Tkl': 'Tackle',
    'Int': 'Interception',
    'sh': 'Short',
    'ass': 'Assist',
    'kp': 'Key pass',
    'l': 'Long',
    'm': 'Medium',
    'HT': 'Half Time',
    'FT': 'Full Time',
    'KO': 'Kick Off'
}

df['Subcategory'] = df['Subcategory'].replace(clean_sc)

#Clean Result Column
clean_result = {
    'oob': 'Out Of Bounds',
    'l': 'Lost',
    'w': 'Won',
    's': 'Successful',
    'u': 'Unsuccessful',
    'c': 'Complete',
    'i': 'Incomplete',
    'goal': 'Goal',
    
}

df['Result'] = df['Result'].replace(clean_result)

#Select columns to return
df = df[['Tournament', 'Date', 'Team', 'Opponent', 'Player', 'Category', 'Subcategory', 'Result', 'period', 'Timestamp', 'X', 'Y', 'X2', 'Y2' ]]
# Create a list of values to drop
values_to_drop = ['Half Time', 'Full Time', 'Kick Off']
# Filter the DataFrame and drop the rows with the specified values
df = df[~df['Subcategory'].isin(values_to_drop)]

# Prompt the user for the filename to save the processed DataFrame as a new CSV file
output_filename = input("Enter the filename to save the processed DataFrame as a new CSV file: ") + '.csv'
# Check if the input filename and output filename are the same
if output_filename == filename:
    print("Error: The output filename cannot be the same as the input filename.")
    print("Please provide a different output filename.")
    exit()

# Save the DataFrame to the specified filename
df.to_csv(output_filename, index=False)
print(f"DataFrame saved to {output_filename}")
