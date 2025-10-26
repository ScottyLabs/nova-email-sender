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

    with open('provisioning-key.txt') as f:
        provisioning_key = f.read().strip()

    with open('key-hashes.txt') as f:
        hashes = f.read().splitlines()

        for hash in hashes:
            disable_hash(hash, enable_instead, provisioning_key)

    print("Done.")