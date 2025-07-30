import csv
import os
import requests
from bs4 import BeautifulSoup
from zenml import step

# Helper to split name
def split_name(full_name):
    parts = full_name.strip().split()
    if len(parts) >= 2:
        return parts[0], " ".join(parts[1:])
    return parts[0], ""

@step
def get_or_create_user(user_full_name: str) -> dict:
    users_file = "users.csv"
    if not os.path.exists(users_file):
        with open(users_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "first_name", "last_name", "full_name"])
    first_name, last_name = split_name(user_full_name)
    user_id = f"{first_name.lower()}_{last_name.lower().replace(' ', '_')}"
    with open(users_file, mode='r') as f:
        users = list(csv.DictReader(f))
        for user in users:
            if user["full_name"].strip().lower() == user_full_name.strip().lower():
                return user
    with open(users_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, first_name, last_name, user_full_name])
    return {
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "full_name": user_full_name
    }

@step
def crawl_links(user: dict, links: list[str]) -> str:
    crawled_file = "crawled_data.csv"
    if not os.path.exists(crawled_file):
        with open(crawled_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "full_name", "link", "content"])
    for link in links:
   
        try:
            r = requests.get(link, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title Found"
        except Exception as e:
            title = f"Failed to retrieve: {e}"
        with open(crawled_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user["user_id"], user["full_name"], link, title])
    return "Crawling done!"
