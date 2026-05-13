import os
import requests

def disable_hash(hash: str, enable_instead: bool, provisioning_key: str) -> None:
    base_url = "https://openrouter.ai/api/v1/keys"

    response = requests.patch(
        f"{base_url}/{hash}",
        headers={
            "Authorization": f"Bearer {provisioning_key}",
            "Content-Type": "application/json"
        },
        json={
            "disabled": not enable_instead,
        }
    )

    if not response.ok:
        print(f"Failed to {"enable" if enable_instead else "disable"} hash: {hash}")
        print(response, response.content)

if __name__ == "__main__":
    enable_instead_prompt = input("Enable instead [y/N]:").lower()
    if enable_instead_prompt == "y":
        enable_instead = True
    else:
        enable_instead = False

    provisioning_key = os.getenv("OPENROUTER_PROVISIONING_KEY")
    if not provisioning_key:
        print("No OpenRouter key found. Provide OPENROUTER_PROVISIONING_KEY environment variable.")
        exit(1)

    with open('key-hashes.txt') as f:
        hashes = f.read().splitlines()

        for hash in hashes:
            disable_hash(hash, enable_instead, provisioning_key)

    print("Done.")