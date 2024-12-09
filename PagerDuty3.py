import requests
import csv
import json
import pandas as pd

# Function to clean up improperly escaped JSON strings
def fix_json_string(json_string):
    # Replace incorrectly escaped backslashes with single backslashes
    # This fixes escaping issues where we have \\ instead of \
    fixed_string = json_string.replace(r'\\', r'\\')  # Fix double slashes
    # Ensure internal quotes are correctly escaped
    fixed_string = fixed_string.replace(r'\"', '"')  # Fix escaped quotes
    return fixed_string

# Read the CSV file with proper handling of quoted fields
# Read the CSV file, ensuring proper data types for each column
df = pd.read_csv('services.csv', delimiter=',', quotechar='"', dtype={'auto_resolve_timeout': int, 'escalation_policy': str})
df = df.reset_index(drop=True)

# Inspect the DataFrame to check the contents
print(df[['auto_resolve_timeout', 'escalation_policy']])

token = "u+ZN7H_wCSzBzPrCy7tg"

 # Read the header row
titles = df.columns.tolist()

# Iterate through the DataFrame rows
for idx, row in df.iterrows():
    # Get the raw JSON strings
    auto_resolve_timeout = row['auto_resolve_timeout']
    escalation_policy = row['escalation_policy']

    # Clean the JSON strings
    auto_resolve_timeout_cleaned = fix_json_string(auto_resolve_timeout)
    escalation_policy_cleaned = fix_json_string(escalation_policy)

    # Try parsing the cleaned JSON strings
    try:
        auto_resolve_timeout_json = json.loads(auto_resolve_timeout_cleaned)
        escalation_policy_json = json.loads(escalation_policy_cleaned)

        # Print the parsed JSON for verification
        print(f"Row {idx}:")
        print(f"auto_resolve_timeout: {auto_resolve_timeout_json}")
        print(f"escalation_policy: {escalation_policy_json}")
        print()

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        continue  # Handle this row if JSON is malformed

    url = 'https://api.pagerduty.com/services'

    # Set up the headers with the Authorization token
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2'
    }

    # get data by reading from the csv file
    data = {}
    # Loop through the rows of the dataframe, starting from the second row
    for idx, row in df.iloc[1:].iterrows():  # df.iloc[1:] skips the first row
        for i, item in enumerate(row):
            print(len(row))
            # Map each column to the corresponding field name from the header
            if titles[i] == "auto_resolve_timeout":
                print(item)
                data[titles[i]] = int(item)
            elif titles[i] == "escalation+policy":
                data[titles[i]] = escalation_policy
            else:
                data[titles[i]] = item

        # Print or store the data as needed
        print(data)

        print(len(row))

        # Print the data being sent (for debugging purposes)
        print("Data being sent:", json.dumps(data, indent=4))

        # Make the POST request with the token in the headers
        response = requests.post(url, json=data, headers=headers)

        print(response)

        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print(f"Error: {response.status_code}")
            print(response.text)