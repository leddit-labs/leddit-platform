export const BASE_API_GATEWAY =
  import.meta.env.VITE_API_GATEWAY ?? "http://localhost:9080";

const API_PREFIX = "/api/v1"; // if we have a version or other prefix. for example api/v1

export const endpoints = {
  //here u go wenmin add your endpoints here pls
  auth: {
    login: "",
    logout: "",
  },

  posts: {
    all: `${API_PREFIX}/posts`,
    create: `${API_PREFIX}/posts`,
    byId: (id: string) => `${API_PREFIX}/posts/${id}`,
    update: (id: string) => `${API_PREFIX}/posts/${id}`,
    delete: (id: string) => `${API_PREFIX}/posts/${id}`,
  },

  communities: {

  },

  //and so on
  //and so on
};
