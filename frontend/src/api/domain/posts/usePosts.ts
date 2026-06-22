import { useQuery } from "@tanstack/react-query";
import { getPosts } from "./postService";

export function usePosts(page: number, size: number) {
  return useQuery({
    queryKey: ["posts", page, size],
    queryFn: () => getPosts({ page, size }),
  });
}