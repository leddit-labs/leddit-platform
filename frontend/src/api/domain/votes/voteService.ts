import api from "../../client";
import { endpoints } from "../../endpoints";

export const voteService = {
  async getPostVotes(postId: string) {
    try {
      const res = await api.get(endpoints.votes.postVotes(postId));
      return res.data;
    } catch (err: any) {
      if (err.response?.status === 404) {
        return { score: 0 };
      }
      throw err;
    }
  },

  async getCommentVotes(commentId: string) {
    const res = await api.get(endpoints.votes.commentVotes(commentId));
    return res.data;
  },

  async getMyPostVote(postId: string, userId: string) {
    const res = await api.get(endpoints.votes.myPostVote(postId, userId));
    return res.data;
  },

  async votePost(postId: string, value: number) {
    const res = await api.post(endpoints.votes.votePost(postId), {
      value,
    });

    return res.data;
  },

  async voteComment(commentId: string, value: number) {
    const res = await api.post(endpoints.votes.voteComment(commentId), {
      value,
    });

    return res.data;
  },
};