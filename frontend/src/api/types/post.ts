export type Post = {
  id: string; //UUID
  title: string;
  content: string;
  author_id: string;
  created_at: string;
};

export type CreatePostRequest = {
  title: string;
  content: string;
};

export type UpdatePostRequest = {
  title?: string;
  content?: string;
};
