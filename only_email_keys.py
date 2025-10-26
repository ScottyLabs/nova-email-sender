import csv
import os

from generate_and_email_keys import read_teams, send_api_key_to_emails

if __name__ == "__main__":
    try:
        with open('mailgun-key.txt', 'r') as file:
            mailgun_key = file.read()
    except FileNotFoundError:
        print("No mailgun key found. Provide mailgun-key.txt file.")

    teams = read_teams('teams.csv')

    if not os.path.isfile('team-keys.csv'):
        print("No team-keys.csv found. Create team-keys.csv first.")
        exit(1)

    with open('team-keys.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['Key']
            team_name = row['Team Name']
            emails = teams[team_name]
            send_api_key_to_emails(key, team_name, emails, mailgun_key)

    print("Done.")