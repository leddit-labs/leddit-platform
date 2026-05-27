export interface VoteSummary {
  post_id: string;
  upvotes: number;
  downvotes: number;
  score: number;
}

export interface CommentVoteSummary {
  comment_id: string;
  upvotes: number;
  downvotes: number;
  score: number;
}

export interface UserVote {
  value: number; // -1 | 0 | 1
}

export interface VoteCreate {
  user_id: string;
  value: 1 | -1;
}