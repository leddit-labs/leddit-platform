import api from "../../client";
import { endpoints } from "../../endpoints";
import type {
  VoteSummary,
  CommentVoteSummary,
  UserVote,
  VoteCreate,
} from "./vote";

export const voteService = {
  async getPostVotes(postId: string): Promise<VoteSummary> {
    try {
      const res = await api.get<VoteSummary>(endpoints.votes.postVotes(postId));
      return res.data;
    } catch (err: any) {
      if (err.response?.status === 404) {
        return {
          post_id: postId,
          upvotes: 0,
          downvotes: 0,
          score: 0,
        };
      }
      throw err;
    }
  },

  async getCommentVotes(commentId: string): Promise<CommentVoteSummary> {
    const res = await api.get<CommentVoteSummary>(
      endpoints.votes.commentVotes(commentId),
    );
    return res.data;
  },

  async getMyPostVote(postId: string, userId: string): Promise<UserVote> {
    const res = await api.get<UserVote>(
      endpoints.votes.myPostVote(postId, userId),
    );
    return res.data;
  },

  async votePost(
    postId: string,
    value: 1 | -1,
    user_id: string,
  ): Promise<void> {
    await api.post(endpoints.votes.votePost(postId), {
      user_id,
      value,
    } satisfies VoteCreate);
  },

  async voteComment(
    commentId: string,
    value: 1 | -1,
    user_id: string,
  ): Promise<void> {
    await api.post(endpoints.votes.voteComment(commentId), {
      user_id,
      value,
    } satisfies VoteCreate);
  },
};
