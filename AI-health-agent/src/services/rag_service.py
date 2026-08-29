import hashlib

import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGService:
    """Build and query report-specific vector stores."""

    ANALYSIS_QUERIES = [
        "complete blood count CBC abnormalities hemoglobin WBC RBC platelets",
        "glucose HbA1c diabetes metabolic panel electrolyte abnormalities",
        "kidney function creatinine urea BUN eGFR renal markers",
        "liver function ALT AST ALP bilirubin albumin hepatic markers",
        "lipid profile cholesterol LDL HDL triglycerides cardiovascular risk",
        "infection inflammation ESR CRP neutrophils lymphocytes immune markers",
        "thyroid vitamins nutritional deficiencies iron B12 vitamin D ferritin",
    ]

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def get_report_key(self, text_content):
        normalized = (text_content or "").strip().encode("utf-8")
        return hashlib.sha256(normalized).hexdigest()

    def get_or_create_vector_store(self, text_content, session_id=None):
        if not text_content or not text_content.strip():
            text_content = "No report context available."

        report_key = self.get_report_key(text_content)
        cache_key = f"{session_id or 'default'}:{report_key}"

        if (
            st.session_state.get("vector_store_key") == cache_key
            and "vector_store" in st.session_state
        ):
            return st.session_state.vector_store

        chunks = self.text_splitter.split_text(text_content)
        if not chunks:
            chunks = [text_content]

        vector_store = FAISS.from_texts(chunks, self.embeddings)
        st.session_state.vector_store = vector_store
        st.session_state.vector_store_key = cache_key
        st.session_state.current_report_key = report_key
        return vector_store

    def retrieve_context(self, vector_store, query, k=4):
        if not vector_store:
            return ""

        try:
            retriever = vector_store.as_retriever(search_kwargs={"k": k})
            if hasattr(retriever, "invoke"):
                docs = retriever.invoke(query)
            else:
                docs = retriever.get_relevant_documents(query)
            return "\n\n".join(doc.page_content for doc in docs)
        except Exception:
            return ""

    def retrieve_analysis_context(self, vector_store):
        sections = []

        for query in self.ANALYSIS_QUERIES:
            context = self.retrieve_context(vector_store, query, k=3)
            if context:
                sections.append(f"## Retrieved context for: {query}\n{context}")

        return "\n\n".join(self._deduplicate_sections(sections))

    def _deduplicate_sections(self, sections):
        seen = set()
        unique_sections = []

        for section in sections:
            section_key = hashlib.sha256(section.encode("utf-8")).hexdigest()
            if section_key not in seen:
                seen.add(section_key)
                unique_sections.append(section)

        return unique_sections
