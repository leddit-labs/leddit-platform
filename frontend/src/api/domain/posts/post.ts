export type Post = {
  u_id: string;
  title: string;
  content: string;
  community_id: string;
  author_id: string;
  created_at: string;
};

export type CreatePostRequest = {
  community_id: string;
  author_id: string;
  title: string;
  content: string;
};

export type UpdatePostRequest = {
  title?: string;
  content?: string;
};
