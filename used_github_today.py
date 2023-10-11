import requests
import sys
from datetime import datetime, timedelta
from pprint import pprint


def has_contributed_today(username):
    response = requests.get(f"https://api.github.com/users/{username}/events")
    response.raise_for_status()

    events = response.json()

    now = datetime.now()
    one_day_ago = now - timedelta(days=1)

    def f_created_at(event):
        return datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    contributions = [e for e in events if f_created_at(e) > one_day_ago]
    pprint([{"type": c["type"], "repo": c["repo"]["name"]} for c in contributions])
    return contributions


def main():
    if len(sys.argv) != 2:
        print("Usage: python used_github_today.py <username>")
        sys.exit(1)

    username = sys.argv[1]

    if contribs := has_contributed_today(username):
        print(
            f"{username} has contributed {len(contribs)} to GitHub in the last 24 hours."
        )
    else:
        print(f"{username} has not contributed to GitHub in the last 24 hours.")


if __name__ == "__main__":
    main()
