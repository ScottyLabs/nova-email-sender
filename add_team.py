from pathlib import Path

from generate_and_email_keys import *

if __name__ == "__main__":
    team_name = input("Enter team name: ")
    emails: list[str] = []

    while True:
        email = input("Enter email: ")
        if email == "":
            break
        emails.append(email)

    print("Adding to teams.csv")

    create_new = not Path('teams.csv').is_file()

    with open('teams.csv', 'a') as teams_file:
        if create_new:
            teams_file.write("Team,Email\n")
        for email in emails:
            teams_file.write(f"{email},{team_name}\n")

    print("Done")

    generate_and_send_key_to_teams({team_name: emails})

    print("Done")