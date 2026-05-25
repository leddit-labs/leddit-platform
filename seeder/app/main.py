import asyncio

from app.health import wait_for_services
from app.generator import user, community, post, comment, vote
from app.state import SeedState

from app.clients.users import UserClient
from app.clients.communities import CommunityClient
from app.clients.posts import PostClient
from app.clients.comments import CommentClient
from app.clients.votes import VoteClient
from app.config import endpoints

async def run():
    print("Seeder starting...")
    await wait_for_services()

    state = SeedState()

    users = UserClient(endpoints.USERS)
    communities = CommunityClient(endpoints.COMMUNITIES)
    posts = PostClient(endpoints.POSTS)
    comments = CommentClient(endpoints.COMMENTS)
    votes = VoteClient(endpoints.VOTES)

    """

    # -------------------
    # 1. USERS
    # -------------------
    for _ in range(5):
        u = await users.create(user())
        state.users.append(u)

    # -------------------
    # 2. COMMUNITIES
    # -------------------
    for _ in range(3):
        c = await communities.create(community())
        state.communities.append(c)

    # -------------------
    # 3. POSTS
    # -------------------
    for c in state.communities:
        for u in state.users:
            p = await posts.create(post(c["id"], u["id"]))
            state.posts.append(p)

    # -------------------
    # 4. COMMENTS
    # -------------------
    for p in state.posts:
        for u in state.users:
            cm = await comments.create(comment(p["id"], u["id"]))
            state.comments.append(cm)

    # -------------------
    # 5. VOTES
    # -------------------
    for p in state.posts:
        for u in state.users:
            await votes.create({
                "post_id": p["id"],
                "user_id": u["id"],
                "value": vote()["value"]
            })
"""
    print("done for now")
    


if __name__ == "__main__":
    asyncio.run(run())