from pathlib import Path
import zipfile

from send2trash import send2trash

if __name__ == "__main__":
    archive_name: str = input("Archive name (.zip): ").removesuffix(".zip")
    if len(archive_name) == 0:
        raise ValueError(f'Invalid archive name "{archive_name}"')
    archive_name = f'{archive_name}.zip'
    if Path(archive_name).is_file():
        if input(f'"{archive_name}" already exists. Overwrite? (y|N): ').lower() != "y":
            print("Archiving cancelled")
            exit()

    store_api_keys: bool = input("Archive (and optionally remove) .env file? (not recommended) (y|N): ").lower() == "y"

    files_to_archive: list[str] = []

    for potential_file in ["key-hashes.txt", "team-keys.csv", "teams.csv"] + \
        ([".env"] if store_api_keys else []):
        if Path(potential_file).is_file():
            files_to_archive.append(potential_file)

    if len(files_to_archive) == 0:
        print("No files to archive, exiting")
        exit(1)

    print(f"Discovered {len(files_to_archive)} files, archiving...")

    with zipfile.ZipFile(archive_name, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_archive:
            zipf.write(file)

    if input("Archive done, trash archived files? (y|N): ").lower() == "y":
        print("Trashing archived files...")
        for file in files_to_archive:
            send2trash(file)

    print(f'Done! Archive created at "{archive_name}"')
