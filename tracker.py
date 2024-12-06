import twikit
import time
import json
import os

# Initialize Twikit client
client = twikit.Client(bearer_token="YOUR_BEARER_TOKEN")

# Read tracked accounts from a file
with open("accounts.txt", "r") as f:
    tracked_accounts = [line.strip() for line in f.readlines()]

# Load previous followings from file (if available)
if os.path.exists("followings.json"):
    with open("followings.json", "r") as f:
        previous_followings = json.load(f)

# Fetch and compare followings
for account in tracked_accounts:
    print(f"Fetching followings for {account}...")
    try:
        following = client.get_user_following(account)

        # Extract new followings
        previous_set = set(previous_followings.get(account, []))
        current_set = set(following['data'])  # Assuming the data contains user IDs or handles
        new_followings = current_set - previous_set

        # Output new follows
        if new_followings:
            print(f"New followings for {account}: {new_followings}")
        else:
            print(f"No new followings for {account}")

        # Save current followings
        previous_followings[account] = list(current_set)

        # Save the updated followings to file
        with open("followings.json", "w") as f:
            json.dump(previous_followings, f)

    except Exception as e:
        print(f"Error fetching followings for {account}: {e}")

    # Sleep to avoid hitting rate limits
    time.sleep(5)
