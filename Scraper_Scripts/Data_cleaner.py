import pandas as pd
import re

# Load your dataset
df = pd.read_csv('emails (1).csv')

# Function to validate an email address
def is_valid_email(email):
    # Regular expression for validating an email
    regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return bool(re.match(regex, email, re.I))
# Replace 'email_column_name' with the actual column name containing emails
email_column_name = 'support@momjunction.com'

# Apply the validation function to filter out invalid emails
df['valid_email'] = df[email_column_name].apply(lambda x: is_valid_email(x) if pd.notnull(x) else False)

# Print the number of valid and invalid emails
print(f"Valid emails: {df['valid_email'].sum()}")
print(f"Invalid emails: {len(df) - df['valid_email'].sum()}")

# Keep only the valid emails
df = df[df['valid_email'] == True]

# Drop the temporary 'valid_email' column
df.drop('valid_email', axis=1, inplace=True)

# Remove duplicates
df.drop_duplicates(subset=email_column_name, keep='first', inplace=True)

# Print the DataFrame to verify its contents
print(df)

# Save the cleaned dataset
df.to_csv('cleaned_dataset.csv', index=False)