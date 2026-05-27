export interface VoteSummary {
  upvotes: number;
  downvotes: number;
  score: number;
}

export interface UserVote {
  value: number; // -1 | 0 | 1
}

export interface VoteCreate {
  user_id: string;
  value: number;
}