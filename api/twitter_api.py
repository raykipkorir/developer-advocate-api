import csv
from typing import Callable

import requests
from django.conf import settings

from .models import Advocate, Company

all_usernames = []
#scraped data using selenium
def get_usernames() -> list:
    with open('api/usernames.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for username in csv_reader:
            if username:
                all_usernames.append(username[0][1:])
    return all_usernames

# getting user or users with username
def get_user(url: str, payload: dict, header: dict) -> dict:
    response = requests.get(url, headers=header, params=payload).json()
    return response['data']

def get_companies(bio: str) -> str:
    bio = bio.lower()
    bio_list = bio.split()
    for word in bio_list:
        if word == "advocate":
            try:
                company = bio_list[bio_list.index(word) + 1]
                if not company.startswith("@"):
                    company = bio_list[bio_list.index(word) + 2]
                    if not company.startswith("@"):
                        return
                return company[1:].strip(".").strip(",")
            except:
                return

def query_company(company: str, header: dict):
    try:
        url = "https://api.twitter.com/2/users/by/username/" + company
        payload = {'user.fields':'description,name,username'}
        response = requests.get(url, params=payload, headers=header).json()
        data = response['data']
        instance, created = Company.objects.get_or_create(
            id = data['id'],
            username = data['username'],
            name = data.get('name'),
            bio = data.get('description', 'null'),
        )
        return instance
    except:
        return 

#used initially to populate database
def populate_database(url, payload, header):
    for username in get_usernames():
        data = get_user(url, payload, header)
        companies = get_companies(data['description'])
        try:
            obj, created = Advocate.objects.update_or_create(
                id = data['id'],
                username = data['username'],
                name = data['name'],
                bio = data['description'],
                location = data.get('location', 'null'),
                twitter_url = f"https://twitter.com/{data['username']}",
                profile_pic_url = data.get('profile_image_url', 'null'),
                following_count = data['public_metrics']['following_count'],
                followers_count = data['public_metrics']['followers_count'],
                company = query_company(companies, header),
            )
        except:
            pass

#update user info with every api call
def update_user_info(username: str, url: str, payload: dict, header: dict):
    if username:
        data = get_user(url, payload, header)
        companies = get_companies(data['description'])
        Advocate.objects.filter(username=username).update(
            id = data['id'],
            username = data['username'],
            name = data['name'],
            bio = data['description'],
            location = data.get('location', 'null'),
            twitter_url = f"https://twitter.com/{data['username']}",
            profile_pic_url = data.get('profile_image_url', 'null'),
            following_count = data['public_metrics']['following_count'],
            followers_count = data['public_metrics']['followers_count'],
            company = query_company(companies, header),
        )

def main(username=None) -> None:
    header = {"Authorization": "Bearer " + settings.TWITTER_API_KEY}
    payload = {
                'user.fields': 'description,location,name,profile_image_url,username,public_metrics',
            }
    url = "https://api.twitter.com/2/users/by/username/" + username
    
    update_user_info(username, url, payload, header)
