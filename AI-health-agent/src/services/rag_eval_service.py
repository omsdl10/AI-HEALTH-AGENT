import re
from datetime import datetime

import streamlit as st


class RAGEvalService:
    """Lightweight, local RAG evaluation for retrieval and grounding checks."""

    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "with",
        "you",
        "your",
    }

    def evaluate(self, query, retrieved_context, answer, mode, session_id=None):
        query_tokens = self._tokens(query)
        context_tokens = self._tokens(retrieved_context)
        answer_tokens = self._tokens(answer)

        retrieval_coverage = 1.0 if context_tokens else 0.0
        query_context_overlap = self._overlap(query_tokens, context_tokens)
        answer_grounding = self._overlap(answer_tokens, context_tokens)
        answer_relevance = self._overlap(answer_tokens, query_tokens)

        score = (
            retrieval_coverage * 0.25
            + query_context_overlap * 0.25
            + answer_grounding * 0.35
            + answer_relevance * 0.15
        )

        result = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "session_id": session_id,
            "mode": mode,
            "query": query,
            "score": round(score * 100),
            "retrieval_coverage": round(retrieval_coverage * 100),
            "query_context_overlap": round(query_context_overlap * 100),
            "answer_grounding": round(answer_grounding * 100),
            "answer_relevance": round(answer_relevance * 100),
            "context_chars": len(retrieved_context or ""),
            "verdict": self._verdict(score),
        }

        self.store_result(result)
        return result

    def store_result(self, result):
        if "rag_eval_results" not in st.session_state:
            st.session_state.rag_eval_results = []
        st.session_state.rag_eval_results.append(result)

    def get_results(self, session_id=None):
        results = st.session_state.get("rag_eval_results", [])
        if not session_id:
            return results
        return [result for result in results if result.get("session_id") == session_id]

    def summarize(self, session_id=None):
        results = self.get_results(session_id)
        if not results:
            return None

        avg_score = sum(item["score"] for item in results) / len(results)
        avg_grounding = sum(item["answer_grounding"] for item in results) / len(results)
        avg_overlap = sum(item["query_context_overlap"] for item in results) / len(results)

        return {
            "count": len(results),
            "avg_score": round(avg_score),
            "avg_grounding": round(avg_grounding),
            "avg_query_context_overlap": round(avg_overlap),
            "latest": results[-1],
        }

    def _tokens(self, text):
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9_+-]*|\d+(?:\.\d+)?", text or "")
        return {
            word.lower()
            for word in words
            if len(word) > 2 and word.lower() not in self.STOPWORDS
        }

    def _overlap(self, source_tokens, target_tokens):
        if not source_tokens:
            return 0.0
        return len(source_tokens.intersection(target_tokens)) / len(source_tokens)

    def _verdict(self, score):
        if score >= 0.75:
            return "Good"
        if score >= 0.5:
            return "Fair"
        return "Needs attention"
