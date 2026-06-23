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
from app.clients.auth import get_token


async def run():
    print("Seeder starting...")
    await wait_for_services()

    state = SeedState() # will save the current state of every created object in all DB's

    
    # TODO users should also be created here and added to the state together with their token
    
    # -------------------
    # USERS
    # -------------------
    # for _ in range(5):
    #    u = await users.create(user())
    #    state.users.append(u)

    # 1. GET TOKEN
    current_token = await get_token("nademtis", "nademtis")
    print("token: ", current_token)
    user_client = UserClient(endpoints.USERS, current_token)
    
    # get user and append
    current_user = await user_client.get_profile()
    state.users.append(current_user)

    # -------------------
    # 2. COMMUNITIES
    # -------------------
    communities = CommunityClient(endpoints.COMMUNITIES, current_token)
    for _ in range(1):
        c = await communities.create(community())
        state.communities.append(c)

    # -------------------
    # 3. POSTS
    # -------------------
    # every user makes 1 post to every community
    posts = PostClient(endpoints.POSTS, current_token)

    for c in state.communities:
        for u in state.users:
            p = await posts.create(post(c["id"], u["id"]))
            state.posts.append(p)

    print(state)
    """
    
    
    comments = CommentClient(endpoints.COMMENTS, token)
    votes = VoteClient(endpoints.VOTES, token)








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
