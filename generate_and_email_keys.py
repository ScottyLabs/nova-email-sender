import csv
import os.path

import requests

def read_teams(file: str) -> dict[str, list[str]]:
    with open(file) as f:
        reader = csv.DictReader(f)

        result: dict[str, list[str]] = {}

        for row in reader:
            if not row["Team"] in result:
                result[row["Team"]] = []
            result[row["Team"]].append(row["Email"])

        return result


def generate_api_key(team_name: str, provisioning_key: str) -> str:
    base_url = "https://openrouter.ai/api/v1/keys"
    response = requests.post(
        f"{base_url}",
        headers={
            "Authorization": f"Bearer {provisioning_key}",
            "Content-Type": "application/json",
        },
        json={
            "name": f"Team {team_name}",
            "limit": 30
        }
    )
    # print(response)
    response.raise_for_status()

    response_json = response.json()
    with open("key-hashes.txt", "a") as f:
        f.write(f"{response_json['data']['hash']}\n")
    with open("team-keys.csv", "a") as f:
        f.write(f"{team_name},{response_json['key']},{response_json['data']['hash']}\n")

    print(f"Created API key for team {team_name}")
    return response_json['key']

def send_api_key_to_emails(key: str, team_name: str, emails: list[str], mailgun_key: str) -> None:
    email_contents = f"Hello {team_name},\n\nBelow is your OpenRouter API key for Nova.\n\n{key}\n\nWe're so excited to see what you'll do. Good luck!"

    mail_domain = "sandbox466956565fcc40a8ac45c66988151339.mailgun.org"
    url = f"https://api.mailgun.net/v3/{mail_domain}/messages"
    payload = {
        "from": f"Nova API Key Distributor <postmaster@{mail_domain}>",
        "to": emails,
        "subject": "Your OpenRouter API Key For Nova",
        "text": email_contents,
    }
    response = requests.post(
        url,
        headers={
            "Authorization": f"Basic {mailgun_key}",
        },
        data=payload,
        files=[]
    )
    if response.status_code != requests.codes.ok:
        print(f"Failed to send email to {emails}", response, response.content)
    else:
        print(f"Email sent to {emails}", response, response.content)

if __name__ == '__main__':
    try:
        with open('provisioning-key.txt', 'r') as file:
            provisioning_key = file.read()
    except FileNotFoundError:
        print("No provisioning key found. Provide provisioning_key.txt file.")
        exit(1)
    try:
        with open('mailgun-key.txt', 'r') as file:
            mailgun_key = file.read()
    except FileNotFoundError:
        print("No mailgun key found. Provide mailgun-key.txt file.")

    teams = read_teams('teams.csv')

    if not os.path.isfile('team-keys.csv'):
        print("Creating team-keys.csv file.")
        with open('team-keys.csv', 'a') as f:
            f.write("Team Name,Key,Hash\n")
    else:
        print("Team-keys.csv already exists. Appending to end.")

    for team_name, emails in teams.items():
        key = generate_api_key(team_name, provisioning_key)
        send_api_key_to_emails(key, team_name, emails, mailgun_key)

    print("Done.")