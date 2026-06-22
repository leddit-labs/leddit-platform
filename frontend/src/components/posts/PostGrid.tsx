import { SimpleGrid } from "@chakra-ui/react";
import type { Post } from "../../api/domain/posts/post";
import PostCard from "./PostCard";
import PostSkeleton from "./PostSkeleton";

type Props = {
  posts?: Post[];
  isLoading: boolean;
};

export default function PostGrid({ posts = [], isLoading }: Props) {
  if (isLoading) {
    return (
      <SimpleGrid columns={1} spacing={3} mt={4}>
        {Array.from({ length: 5 }).map((_, i) => (
          <PostSkeleton key={i} />
        ))}
      </SimpleGrid>
    );
  }

  return (
    <SimpleGrid columns={1} spacing={3} mt={4}>
      {posts.map((post) => (
        <PostCard key={post.u_id} post={post} />
      ))}
    </SimpleGrid>
  );
}