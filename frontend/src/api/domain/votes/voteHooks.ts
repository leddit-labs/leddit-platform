// src/api/domain/votes/useVotes.ts
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { voteService } from "./voteService";

export function usePostVotes(postId: string) {
  return useQuery({
    queryKey: ["postVotes", postId],
    queryFn: () => voteService.getPostVotes(postId),
  });
}

export function useVotePost(postId: string) {
  const queryClient = useQueryClient();

  
  //need the user ID from user service? maybe set in Callback.tsx
  const userId = "lmao" // TODO fix me 
  return useMutation({
    mutationFn: (value: 1 | -1) =>
      voteService.votePost(postId, value, userId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["postVotes", postId],
      });
    },
  });
}