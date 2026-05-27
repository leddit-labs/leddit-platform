// src/api/domain/votes/useVotes.ts
import { useQuery } from "@tanstack/react-query";
import { voteService } from "./voteService";

export function usePostVotes(postId: string) {
  return useQuery({
    queryKey: ["postVotes", postId],
    queryFn: () => voteService.getPostVotes(postId),
  });
}