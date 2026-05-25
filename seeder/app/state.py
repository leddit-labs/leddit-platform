class SeedState:
    def __init__(self):
        self.users = []
        self.communities = []
        self.posts = []
        self.comments = []
        self.votes = []

    def __repr__(self):
        return (
            f"SeedState("
            f"users={len(self.users)}, "
            f"communities={len(self.communities)}, "
            f"posts={len(self.posts)}, "
            f"comments={len(self.comments)}, "
            f"votes={len(self.votes)})"
        )