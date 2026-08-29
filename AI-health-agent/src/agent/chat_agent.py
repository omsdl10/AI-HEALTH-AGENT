import streamlit as st
from groq import Groq
import os

from services.rag_service import RAGService
from services.rag_eval_service import RAGEvalService


class ChatAgent:
    def __init__(self):
        self.rag_service = RAGService()
        self.rag_eval_service = RAGEvalService()
        api_key = os.environ.get("GROQ_API_KEY", "") or st.secrets["GROQ_API_KEY"]
        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.3-70b-versatile"

    def initialize_vector_store(self, text_content, session_id=None):
        """Create or reuse a vector store from report content."""
        return self.rag_service.get_or_create_vector_store(text_content, session_id)

    def _format_chat_history(self, chat_history):
        """Format chat history for Groq API."""
        messages = []
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        return messages

    def _contextualize_query(self, query, chat_history):
        """Reformulate query considering chat history."""
        if not chat_history:
            return query

        # Build context from recent chat history
        recent_history = chat_history[-4:]  # Last 2 exchanges
        history_text = "\n".join(
            [
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in recent_history
            ]
        )

        contextualize_prompt = f"""Given a chat history and the latest user question, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.

Chat History:
{history_text}

Latest User Question: {query}

Standalone Question:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You reformulate questions to be standalone.",
                    },
                    {"role": "user", "content": contextualize_prompt},
                ],
                temperature=0.1,
                max_tokens=200,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return query  # Fallback to original query

    def get_response(self, query, vectorstore, chat_history=None):
        """Get response using RAG."""
        if chat_history is None:
            chat_history = []

        # 1. Contextualize query based on chat history
        contextualized_query = self._contextualize_query(query, chat_history)

        # 2. Retrieve relevant documents
        try:
            context = self.rag_service.retrieve_context(
                vectorstore, contextualized_query, k=4
            )

            # If context is just placeholder text, set to empty
            if context.strip() == "No report context available.":
                context = ""
        except Exception:
            # If retrieval fails, proceed without context
            context = ""

        # 3. Build prompt with context and chat history
        qa_system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "Use three sentences maximum and keep the answer concise."
        )

        # Format messages for Groq API
        messages = [{"role": "system", "content": qa_system_prompt}]

        # Add chat history
        if chat_history:
            formatted_history = self._format_chat_history(
                chat_history[-6:]
            )  # Last 3 exchanges
            messages.extend(formatted_history)

        # Add context and current query
        if (
            context
            and context.strip()
            and context.strip() != "No report context available."
        ):
            user_message = f"Context:\n{context}\n\nQuestion: {query}"
        else:
            # No report context available, rely on chat history only
            user_message = f"Question: {query}\n\nNote: No report context is available. Please answer based on the chat history."
        messages.append({"role": "user", "content": user_message})

        # 4. Get response from Groq
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            answer = response.choices[0].message.content
            session_id = None
            if st.session_state.get("current_session"):
                session_id = st.session_state.current_session.get("id")
            self.rag_eval_service.evaluate(
                query=contextualized_query,
                retrieved_context=context,
                answer=answer,
                mode="Follow-up chat",
                session_id=session_id,
            )
            return answer
        except Exception as e:
            return f"Error generating response: {str(e)}"
