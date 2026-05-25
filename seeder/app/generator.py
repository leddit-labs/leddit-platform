from faker import Faker
import random

fake = Faker()

def user():
    return {
        "username": fake.user_name(),
        "email": fake.email()
    }

def community():
    return {
        "name": fake.word() + str(random.randint(1000, 9999)),
        "description": fake.text(80)
    }

def post(community_id, user_id):
    post = {
        "community_id": community_id,
        "user_id": user_id,
        "title": fake.sentence(),
        "content": fake.text()
    }
    print(post)
    return post

def comment(post_id, user_id):
    return {
        "post_id": post_id,
        "user_id": user_id,
        "text": fake.sentence()
    }

def vote():
    return {
        "value": random.choice([-1, 1])
    }