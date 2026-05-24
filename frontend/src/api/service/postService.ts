import api from "../client";
import { endpoints } from "../endpoints";
import type {
  Post,
  CreatePostRequest,
  UpdatePostRequest,
  PaginatedPosts,
} from "../types/post";

export async function getPosts(params?: {
  page?: number;
  size?: number;
}): Promise<PaginatedPosts> {
  const res = await api.get<PaginatedPosts>(endpoints.posts.all, {
    params,
  });

  return res.data;
}

export async function getPostById(id: string): Promise<Post> {
  const res = await api.get<Post>(endpoints.posts.byId(id));
  return res.data;
}

export async function createPost(data: CreatePostRequest): Promise<Post> {
  const res = await api.post<Post>(endpoints.posts.create, data);
  return res.data;
}

export async function updatePost(
  id: string,
  data: UpdatePostRequest,
): Promise<Post> {
  const res = await api.put<Post>(endpoints.posts.update(id), data);
  return res.data;
}

export async function deletePost(id: string): Promise<Post> {
  const res = await api.delete<Post>(endpoints.posts.delete(id));
  return res.data;
}
