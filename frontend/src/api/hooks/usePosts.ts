import { useEffect, useState } from "react";
import { getPosts } from "../service/postService";
import type { Post } from "../types/post";

export function usePosts(initialPage = 1) {
  const [posts, setPosts] = useState<Post[]>([]);
  const [page, setPage] = useState(initialPage);
  const [loading, setLoading] = useState(false);

  async function loadPosts(page: number) {
    if (page < 1) return;

    setLoading(true);

    const data: Post[] = await getPosts({ page, size: 3 });

    setPosts(data);
    setPage(page);

    setLoading(false);
  }

  useEffect(() => {
    loadPosts(initialPage);
  }, []);

  return {
    posts,
    page,
    loading,
    loadPosts,
  };
}
