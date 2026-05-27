export const BASE_API_GATEWAY =
  import.meta.env.VITE_API_GATEWAY ?? "http://localhost:9080";

const API_PREFIX = "/api/v1"; // if we have a version or other prefix. for example api/v1

export const endpoints = {
  //here u go wenmin add your endpoints here pls
  auth: {
    login: `${BASE_API_GATEWAY}/auth/protocol/openid-connect/auth`,
    logout: `${BASE_API_GATEWAY}/auth/protocol/openid-connect/logout`,
    token: `${BASE_API_GATEWAY}/auth/protocol/openid-connect/token`,
    register: `${BASE_API_GATEWAY}/auth/protocol/openid-connect/registrations`,
    userinfo: `${BASE_API_GATEWAY}/auth/protocol/openid-connect/userinfo`,
  },

  posts: {
    all: `${API_PREFIX}/posts`,
    create: `${API_PREFIX}/posts`,
    byId: (id: string) => `${API_PREFIX}/posts/${id}`,
    update: (id: string) => `${API_PREFIX}/posts/${id}`,
    delete: (id: string) => `${API_PREFIX}/posts/${id}`,
  },

  communities: {
    all: `${API_PREFIX}/communities`,
    byId: (id: string) => `${API_PREFIX}/communities/${id}`,
  },

  votes: {
    postVotes: (postId: string) => `${API_PREFIX}/votes/posts/${postId}`,

    commentVotes: (commentId: string) =>
      `${API_PREFIX}/votes/comments/${commentId}`,

    myPostVote: (postId: string, userId: string) =>
      `${API_PREFIX}/votes/posts/${postId}/me?user_id=${userId}`,

    myCommentVote: (commentId: string, userId: string) =>
      `${API_PREFIX}/votes/comments/${commentId}/me?user_id=${userId}`,

    votePost: (postId: string) => `${API_PREFIX}/votes/posts/${postId}`,

    voteComment: (commentId: string) =>
      `${API_PREFIX}/votes/comments/${commentId}`,
  },

  //and so on
  //and so on
};
