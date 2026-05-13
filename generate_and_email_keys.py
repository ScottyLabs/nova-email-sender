import csv
import os.path

import requests

def read_teams(file: str) -> dict[str, list[str]]:
    with open(file) as f:
        reader = csv.DictReader(f)

        result: dict[str, list[str]] = {}

        for row in reader:
            if row["Team"] == "" or row["Email"] == "":
                continue

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

    mail_domain = "mail.scottylabs.org"
    url = f"https://api.mailgun.net/v3/{mail_domain}/messages"
    payload = {
        "from": f"Nova API Key Distributor <nova@{mail_domain}>",
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

def read_provisioning_key() -> str:
    key = os.getenv("OPENROUTER_PROVISIONING_KEY")
    if not key:
        print("No provisioning key found. Provide OPENROUTER_PROVISIONING_KEY environment variable.")
        exit(1)
    else:
        return key

def read_mailgun_key() -> str:
    key = os.getenv("MAILGUN_KEY")
    if not key:
        print("No mailgun key found. Provide MAILGUN_KEY environment variable.")
        exit(1)
    else:
        return key

def generate_and_send_key_to_teams(teams: dict[str, list[str]]):
    provisioning_key = read_provisioning_key()
    mailgun_key = read_mailgun_key()

    if not os.path.isfile('team-keys.csv'):
        print("Creating team-keys.csv file.")
        with open('team-keys.csv', 'a') as f:
            f.write("Team Name,Key,Hash\n")
    else:
        print("Team-keys.csv already exists. Appending to end.")

    for team_name, emails in teams.items():
        key = generate_api_key(team_name, provisioning_key)
        send_api_key_to_emails(key, team_name, emails, mailgun_key)

if __name__ == '__main__':
    teams = read_teams('teams.csv')

    generate_and_send_key_to_teams(teams)

    print("Done.")