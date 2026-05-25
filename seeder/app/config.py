import os

class Endpoints:
    USERS = os.getenv("USERS_URL")
    COMMUNITIES = os.getenv("COMMUNITIES_URL")
    POSTS = os.getenv("POSTS_URL")
    COMMENTS = os.getenv("COMMENTS_URL")
    VOTES = os.getenv("VOTES_URL")
    KEYCLOAK = os.getenv("KEYCLOAK_URL")

endpoints = Endpoints()