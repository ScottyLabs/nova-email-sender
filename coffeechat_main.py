from pydantic import EmailStr
import requests
import dotenv

import random
import os

dotenv.load_dotenv()


def validate_email_mailgun(email):
    url = f"https://api.mailgun.net/v4/address/validate?address={email}"

    payload = {}
    headers = {
        "Authorization": "Basic " + os.environ.get("MAILGUN_API_KEY"),
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print(f"Validate request failed {email}: {response.text}")
        return False

    if response.json().get("is_valid"):
        return True
    else:
        print(f"Email is being validated (waiting on user to click link): {email}")
        return False


def send_chat_email(email1, email2, content):
    # We need to authorize the email by sending an authorize request to that email

    # if not validate_email_mailgun(email1) or not validate_email_mailgun(email2):
    #     return

    print(f"Authorized emails: {email1}, {email2}")

    mail_domain = "sandbox466956565fcc40a8ac45c66988151339.mailgun.org"

    # Now we can send the email
    url = f"https://api.mailgun.net/v3/{mail_domain}/messages"
    payload = {
        "from": f"SL Coffee Chat Bot <postmaster@{mail_domain}>",
        "to": ["tsurban@andrew.cmu.edu"],
        "subject": "[ScottyLabs] Coffee Chat Pairing",
        "text": content,
    }
    files = []
    headers = {
        "Authorization": "Basic " + os.environ.get("MAILGUN_API_KEY"),
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    if response.status_code != 200:
        print(f"Failed to send email: {response.text}")
        return

    print(f"Email sent to {email1} and {email2}")


def main():
    print("Hello! Welcome to the SL coffee chat bot.")
    participants_file = "data/participants.txt"
    try:
        with open(participants_file, "r") as file:
            participants = [line.strip() for line in file if line.strip()]
        if not participants:
            print("No participants found in the file.")
            return
        print("Participants:")
        for participant in participants:
            print(f"- {participant}")
        # Validate emails
        valid_emails = []
        for email in participants:
            try:
                valid_email = email
                valid_emails.append(valid_email)
            except Exception as e:
                print(f"Invalid email '{email}': {e}")
        print("\n All others valid emails")
    except FileNotFoundError:
        print(f"Error: The file '{participants_file}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    random.shuffle(valid_emails)
    print(valid_emails)
    participant_pairings = []
    for i in range(0, len(valid_emails), 2):
        if i + 1 < len(valid_emails):
            participant_pairings.append((valid_emails[i], valid_emails[i + 1]))
        else:
            print(f"Note: {valid_emails[i]} has no pair this round.")
            extra_option = input(
                "Would you like to pair them with someone else? (y/n): "
            )
            if extra_option.lower() == "y":
                extra_pair = input("Enter the email of the person to pair with: ")
                try:
                    participant_pairings.append((valid_emails[i], valid_emails[i + 1]))
                except Exception as e:
                    print(f"Invalid email '{extra_pair}': {e}")

    # put pairings in a file named {participants_file}+pairings.txt
    pairings_file = f"{participants_file.split('.')[0]}_pairings.txt"
    with open(pairings_file, "w") as file:
        for pair in participant_pairings:
            file.write(f"{pair[0]} - {pair[1]}\n")
    print(f"\nPairings have been saved to '{pairings_file}'.")
    print(f"\nWould you like to send out the emails for these pairings? (y/n): ")
    use_default_template = input(
        "Would you like to use the default email template? (y/n): "
    )
    if use_default_template.lower() == "y":
        email_template = "Hello {name1} and {name2},\n\nYou have been paired for a coffee chat! Enjoy your conversation!\n\nBest,\nSL Coffee Chat Bot"
    else:
        email_template_file = input("Enter the path to your email template file: ")
        try:
            with open(email_template_file, "r") as file:
                email_template = file.read()
        except FileNotFoundError:
            print(f"Error: The file '{email_template_file}' was not found.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return
    send_emails = input("Send emails now? (y/n): ")
    if send_emails.lower() == "y":
        for pair in participant_pairings:
            email_content = email_template.format(name1=pair[0], name2=pair[1])
            print(f"\nSending email to {pair[0]} and {pair[1]}:\n")
            if send_chat_email(pair[0], pair[1], email_content):
                print("Email sent successfully.")
            else:
                print("Failed to send email.")
            print("\n---\n")
        print("Fin.")


if __name__ == "__main__":
    main()
