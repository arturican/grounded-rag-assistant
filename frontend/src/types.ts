export type HealthResponse = {
  status: string;
};

export type IndexRequest = {
  input_dir: string;
  index_path: string;
};

export type IndexResponse = {
  index_path: string;
  indexed_chunk_count: number;
  indexed_chunk_ids: string[];
};

export type AskRequest = {
  index_path: string;
  query: string;
  top_k?: number;
};

export type AnswerSource = {
  source: string;
  page: number | null;
  chunk_id: string;
};

export type AskResponse = {
  answer: string;
  used_context: boolean;
  sources: AnswerSource[];
};
