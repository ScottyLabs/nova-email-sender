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

    with open('teams.csv', 'a') as teams_file:
        for email in emails:
            teams_file.write(f"{email},{team_name}\n")

    print("Done")

    generate_and_send_key_to_teams({team_name: emails})

    print("Done")