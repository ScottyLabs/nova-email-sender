This is a simple collection of Python scripts we use when running our Nova hackathon to send emails with OpenRouter API keys to teams.

## Getting Started

Prerequisites:
1. Python
2. [uv](https://docs.astral.sh/uv/getting-started/installation/), preferably (see [Without uv](#without-uv) if you want to do it the hard way)

### For all methods
1. Clone/download the repository. Enter the directory where you put it from the terminal.
2. Create a copy of the example `.env` file. Update the values accordingly.

### From the terminal
3. Run a script with `uv run <script-name>`. This will download and setup dependencies on first run.

### From PyCharm
3. Open the project. It should automatically detect the run configurations provided (I am not confident in that statement),
   so you should be able to click one in the upper right corner as a run option (select one not marked `(Python)`).

### Without `uv`
3. Question your decision. `uv` is very nice
4. Create a virtual environment with `python -m venv .venv`. Activate it with `source .venv/bin/activate`[^1].
5. Run `pip install .` to install the dependencies.
6. Either open PyCharm and use the (`(Python)`) run options in the top right, or run `python script <script-name>`.

[^1]: `source .venv/bin/activate.fish` for fish shell, `.venv\Scripts\activate.ps1` for Windows Powershell, `.venv\Scripts\activate.bat` for Windows Command Prompt.
	If you’re using something else, Google it.

## The files to know about

### `.env`

This is where you store the API keys for the services you use.
An example of the two values is provided in [`.env.example`](/.env.example) and below

```env
OPENROUTER_PROVISIONING_KEY=sk-or-v1-s0m3str1ng0f73tt3rsandnumb3rs
MAILGUN_KEY=Y0UsH0u7dchANg3TH1S
```

You’ll need to get a *provisioning* key (not a regular one like those you’ll be generating) from OpenRouter.
This will let you create API keys, and will also be the account where those API keys are stored (it will be billed for their usage).
You’ll also need a MailGun key for sending emails. For ScottyLabs purposes, there may only be one in existence...

This file should only be shared with trusted people.
It will intentionally not show up in source control,
and should almost certainly never be force added to override that unless you really know what you’re doing.

### `teams.csv`

This input file contains a list of all emails with an associated team.
This is where you should provide an initial list of teams.
It follows the `Email,Team` (and should have that header), where many Emails may share the same Team value to indicate teammates.

This is used when generating emails to the teams,
and will be appended to when running [`add_team.py`](#add_teampy) to reflect the new team you added.

### `key-hashes.txt`

This generated file stores the hash (a representation OpenRouter uses to identify a created API key) of every key generated.
It is used when disabling keys with [`disable_all_keys.py`](#disable_all_keyspy)

### `team-keys.csv`

This generated file stores a table of the keys and hashes for teams, in the format `Team Name,Key,Hash`.
This is used to resend emails to teams, and if you need to manually give a team their key.
The hash could also be used some other way to disable or edit a specific team, but this is not functionality in a current script.

## The scripts

### `generate_and_email_keys.py`

This is the main workhorse. This will run through every team given, generate an API key for that team, and send an email to all members with the key.
This is where you should look if you want to customize the email template or change most configuration, as other files mostly reference functions from here.

### `only_email_keys.py`

If (hopefully this is not an issue) emailing fails the first time around, this can run through the teams and email them their keys, without regenerating the keys.
It could probably stand to get functionality for sending to just one team, but for now that functionality does not exist.

### `add_team.py`

This will add a new team. First enter the team name, then enter their emails (one per line, it will keep prompting until you enter an empty line).
Then it will generate a key and send the team their new key, updating [`teams.csv`](#teamscsv) accordingly.

### `disable_all_keys.py`

This script can be used to disable or enable[^2] all the keys distributed.
It will prompt you whether you want to enable instead when it first starts, and then march through its list of "all keys"
(based on [`key-hashes.txt`](#key-hashestxt), so don't delete that) and instruct OpenRouter to either turn off or turn on this API key.
Super useful for after the event (wait until final demos are over, of course) so people don’t keep spending our money.

[^2]: Frantic delirium is the only explanation I have for why this script is named "disable" but can do both.

### `archive_year.py`

Creates a zip archive of the `teams.csv`, `key-hashes.txt`, and `team-keys.csv` files, optionally including the `.env` file
(though this is discourage unless you really don’t trust yourself).
This is useful for saving everything at the end of the year, or for making backups throughout the event.
The script can also optionally move the files it just archived to the trash[^3].

[^3]: I stand by the decision to trash instead of hard delete and the extra dependency this requires.
    Humans are humans, and I may have deleted last year’s data several times over if not for trashing instead of deleting.
    See [13733be](https://github.com/ScottyLabs/nova-email-sender/commit/13733be62f3a106d37e1c9ede8892c901ebfecd9).

## License

This code is available under the [MIT License](https://choosealicense.com/licenses/mit/).
It can be used as is or as a reference, but comes with no guarantees of fitness, correctness, or anything else.
