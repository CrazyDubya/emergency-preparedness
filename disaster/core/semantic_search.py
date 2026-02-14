#!/usr/bin/env python3
"""
Semantic Search for Knowledge Base
Provides intelligent search using embeddings and similarity matching
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import sqlite3

logger = logging.getLogger(__name__)

# Optional imports for ML-based semantic search
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logger.info("NumPy not available - using basic search")

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.info("sentence-transformers not available - using keyword search")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.info("FAISS not available - using brute force similarity")


@dataclass
class SearchResult:
    """A single search result"""
    doc_id: str
    title: str
    content: str
    score: float
    category: str
    file_path: str
    snippet: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """A document in the knowledge base"""
    doc_id: str
    title: str
    content: str
    category: str
    file_path: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class KeywordSearchEngine:
    """
    Simple keyword-based search engine
    Falls back to this when ML libraries aren't available
    """

    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.inverted_index: Dict[str, set] = {}

    def add_document(self, doc: Document):
        """Add a document to the search index"""
        self.documents[doc.doc_id] = doc

        # Build inverted index
        words = self._tokenize(doc.content + " " + doc.title)
        for word in words:
            if word not in self.inverted_index:
                self.inverted_index[word] = set()
            self.inverted_index[word].add(doc.doc_id)

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        import re
        # Convert to lowercase and split on non-alphanumeric
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return [w for w in words if len(w) > 2]  # Filter short words

    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """Search for documents matching query"""
        query_words = set(self._tokenize(query))

        if not query_words:
            return []

        # Score documents by word overlap
        scores: Dict[str, float] = {}

        for word in query_words:
            if word in self.inverted_index:
                for doc_id in self.inverted_index[word]:
                    scores[doc_id] = scores.get(doc_id, 0) + 1

        # Normalize scores
        for doc_id in scores:
            scores[doc_id] /= len(query_words)

        # Sort by score
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Build results
        results = []
        for doc_id, score in sorted_docs[:top_k]:
            doc = self.documents[doc_id]
            snippet = self._extract_snippet(doc.content, query_words)

            results.append(SearchResult(
                doc_id=doc.doc_id,
                title=doc.title,
                content=doc.content,
                score=score,
                category=doc.category,
                file_path=doc.file_path,
                snippet=snippet,
                metadata=doc.metadata
            ))

        return results

    def _extract_snippet(self, content: str, query_words: set,
                        context_chars: int = 150) -> str:
        """Extract a relevant snippet from content"""
        content_lower = content.lower()

        # Find position of first query word
        best_pos = 0
        for word in query_words:
            pos = content_lower.find(word)
            if pos != -1:
                best_pos = pos
                break

        # Extract context around the word
        start = max(0, best_pos - context_chars // 2)
        end = min(len(content), best_pos + context_chars // 2)

        snippet = content[start:end].strip()

        # Clean up snippet boundaries
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."

        return snippet


class SemanticSearchEngine:
    """
    ML-based semantic search engine using sentence embeddings
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2",
                 cache_dir: str = ".search_cache"):
        """
        Initialize semantic search engine

        Args:
            model_name: Name of the sentence-transformers model to use
            cache_dir: Directory for caching embeddings
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.documents: Dict[str, Document] = {}
        self.embeddings: Optional[Any] = None  # NumPy array
        self.doc_ids: List[str] = []
        self.index = None  # FAISS index

        # Load model
        if TRANSFORMERS_AVAILABLE:
            try:
                logger.info(f"Loading embedding model: {model_name}")
                self.model = SentenceTransformer(model_name)
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
                logger.info(f"Model loaded. Embedding dimension: {self.embedding_dim}")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}")
                self.model = None
                self.embedding_dim = 0
        else:
            self.model = None
            self.embedding_dim = 0

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding for text"""
        if self.model is None:
            return None

        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None

    def add_document(self, doc: Document):
        """Add a document to the search index"""
        # Generate embedding if not provided
        if doc.embedding is None and self.model is not None:
            text = f"{doc.title}. {doc.content}"
            doc.embedding = self._get_embedding(text)

        self.documents[doc.doc_id] = doc
        self.doc_ids.append(doc.doc_id)

    def build_index(self):
        """Build the search index after adding all documents"""
        if not NUMPY_AVAILABLE or self.model is None:
            logger.info("Using keyword fallback - no index needed")
            return

        # Collect embeddings
        embeddings_list = []
        valid_doc_ids = []

        for doc_id in self.doc_ids:
            doc = self.documents[doc_id]
            if doc.embedding is not None:
                embeddings_list.append(doc.embedding)
                valid_doc_ids.append(doc_id)

        if not embeddings_list:
            logger.warning("No embeddings available")
            return

        self.doc_ids = valid_doc_ids
        self.embeddings = np.array(embeddings_list, dtype=np.float32)

        # Build FAISS index if available
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings)
            logger.info(f"Built FAISS index with {len(valid_doc_ids)} documents")
        else:
            logger.info(f"Built NumPy index with {len(valid_doc_ids)} documents")

    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """
        Search for documents semantically similar to query

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of SearchResult objects sorted by relevance
        """
        if self.model is None or self.embeddings is None:
            logger.debug("Falling back to keyword search")
            return self._keyword_search(query, top_k)

        # Get query embedding
        query_embedding = self._get_embedding(query)
        if query_embedding is None:
            return self._keyword_search(query, top_k)

        query_embedding = np.array([query_embedding], dtype=np.float32)

        # Search
        if FAISS_AVAILABLE and self.index is not None:
            faiss.normalize_L2(query_embedding)
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.doc_ids)))
            scores = scores[0]
            indices = indices[0]
        else:
            # Brute force cosine similarity
            faiss_normalize = lambda x: x / np.linalg.norm(x, axis=1, keepdims=True)
            normalized_embeddings = faiss_normalize(self.embeddings)
            normalized_query = faiss_normalize(query_embedding)

            similarities = np.dot(normalized_embeddings, normalized_query.T).flatten()
            indices = np.argsort(similarities)[::-1][:top_k]
            scores = similarities[indices]

        # Build results
        results = []
        for idx, score in zip(indices, scores):
            if idx < 0 or idx >= len(self.doc_ids):
                continue

            doc_id = self.doc_ids[idx]
            doc = self.documents[doc_id]

            results.append(SearchResult(
                doc_id=doc.doc_id,
                title=doc.title,
                content=doc.content,
                score=float(score),
                category=doc.category,
                file_path=doc.file_path,
                snippet=self._extract_snippet(doc.content, query),
                metadata=doc.metadata
            ))

        return results

    def _keyword_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Fallback keyword search"""
        engine = KeywordSearchEngine()
        for doc in self.documents.values():
            engine.add_document(doc)
        return engine.search(query, top_k)

    def _extract_snippet(self, content: str, query: str,
                        context_chars: int = 200) -> str:
        """Extract relevant snippet using semantic similarity"""
        # Simple approach: find sentences and return most relevant
        sentences = content.replace('\n', ' ').split('.')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        if not sentences:
            return content[:context_chars] + "..."

        # For now, just return first few sentences
        # TODO: Could enhance with sentence-level semantic search
        snippet = '. '.join(sentences[:2])
        if len(snippet) > context_chars:
            snippet = snippet[:context_chars] + "..."

        return snippet

    def save_index(self, path: str):
        """Save the search index to disk"""
        index_path = Path(path)
        index_path.mkdir(parents=True, exist_ok=True)

        # Save document metadata
        docs_data = {
            doc_id: {
                "title": doc.title,
                "category": doc.category,
                "file_path": doc.file_path,
                "metadata": doc.metadata
            }
            for doc_id, doc in self.documents.items()
        }

        with open(index_path / "documents.json", 'w') as f:
            json.dump(docs_data, f)

        # Save embeddings
        if NUMPY_AVAILABLE and self.embeddings is not None:
            np.save(index_path / "embeddings.npy", self.embeddings)

            with open(index_path / "doc_ids.json", 'w') as f:
                json.dump(self.doc_ids, f)

        logger.info(f"Saved search index to {path}")

    def load_index(self, path: str) -> bool:
        """Load search index from disk"""
        index_path = Path(path)

        if not index_path.exists():
            return False

        try:
            # Load document metadata
            with open(index_path / "documents.json", 'r') as f:
                docs_data = json.load(f)

            # Load embeddings
            if NUMPY_AVAILABLE and (index_path / "embeddings.npy").exists():
                self.embeddings = np.load(index_path / "embeddings.npy")

                with open(index_path / "doc_ids.json", 'r') as f:
                    self.doc_ids = json.load(f)

                # Rebuild FAISS index
                if FAISS_AVAILABLE:
                    self.index = faiss.IndexFlatIP(self.embeddings.shape[1])
                    self.index.add(self.embeddings)

            logger.info(f"Loaded search index from {path}")
            return True

        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            return False


class KnowledgeBaseSearcher:
    """
    High-level interface for searching the knowledge base
    """

    def __init__(self, knowledge_base_path: str,
                 use_semantic: bool = True,
                 cache_dir: str = ".search_cache"):
        """
        Initialize knowledge base searcher

        Args:
            knowledge_base_path: Path to the knowledge base directory
            use_semantic: Whether to use semantic search (if available)
            cache_dir: Directory for caching search index
        """
        self.kb_path = Path(knowledge_base_path)
        self.cache_dir = Path(cache_dir)
        self.use_semantic = use_semantic and TRANSFORMERS_AVAILABLE

        # Initialize search engine
        if self.use_semantic:
            self.engine = SemanticSearchEngine(cache_dir=cache_dir)
        else:
            self.engine = KeywordSearchEngine()

        self._indexed = False

    def index_knowledge_base(self, force_rebuild: bool = False) -> int:
        """
        Index all documents in the knowledge base

        Args:
            force_rebuild: Force rebuilding index even if cached

        Returns:
            Number of documents indexed
        """
        # Check for cached index
        index_cache = self.cache_dir / "kb_index"
        if not force_rebuild and isinstance(self.engine, SemanticSearchEngine):
            if self.engine.load_index(str(index_cache)):
                self._indexed = True
                return len(self.engine.documents)

        # Scan knowledge base
        doc_count = 0

        if not self.kb_path.exists():
            logger.warning(f"Knowledge base path not found: {self.kb_path}")
            return 0

        # Index markdown files
        for md_file in self.kb_path.rglob("*.md"):
            try:
                doc = self._parse_markdown(md_file)
                if doc:
                    self.engine.add_document(doc)
                    doc_count += 1
            except Exception as e:
                logger.warning(f"Failed to index {md_file}: {e}")

        # Index text files
        for txt_file in self.kb_path.rglob("*.txt"):
            try:
                doc = self._parse_text(txt_file)
                if doc:
                    self.engine.add_document(doc)
                    doc_count += 1
            except Exception as e:
                logger.warning(f"Failed to index {txt_file}: {e}")

        # Build index
        if isinstance(self.engine, SemanticSearchEngine):
            self.engine.build_index()
            self.engine.save_index(str(index_cache))

        self._indexed = True
        logger.info(f"Indexed {doc_count} documents from knowledge base")

        return doc_count

    def _parse_markdown(self, file_path: Path) -> Optional[Document]:
        """Parse a markdown file into a Document"""
        try:
            content = file_path.read_text(encoding='utf-8')

            # Extract title from first heading
            lines = content.split('\n')
            title = file_path.stem.replace('_', ' ').title()

            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            # Determine category from path
            category = file_path.parent.name

            # Generate document ID
            doc_id = hashlib.md5(str(file_path).encode()).hexdigest()[:12]

            return Document(
                doc_id=doc_id,
                title=title,
                content=content,
                category=category,
                file_path=str(file_path),
                metadata={
                    "format": "markdown",
                    "size": len(content),
                    "indexed_at": datetime.now().isoformat()
                }
            )

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return None

    def _parse_text(self, file_path: Path) -> Optional[Document]:
        """Parse a text file into a Document"""
        try:
            content = file_path.read_text(encoding='utf-8')

            title = file_path.stem.replace('_', ' ').title()
            category = file_path.parent.name
            doc_id = hashlib.md5(str(file_path).encode()).hexdigest()[:12]

            return Document(
                doc_id=doc_id,
                title=title,
                content=content,
                category=category,
                file_path=str(file_path),
                metadata={
                    "format": "text",
                    "size": len(content),
                    "indexed_at": datetime.now().isoformat()
                }
            )

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return None

    def search(self, query: str, top_k: int = 10,
              category: Optional[str] = None) -> List[SearchResult]:
        """
        Search the knowledge base

        Args:
            query: Search query
            top_k: Number of results to return
            category: Optional category filter

        Returns:
            List of SearchResult objects
        """
        if not self._indexed:
            self.index_knowledge_base()

        results = self.engine.search(query, top_k * 2 if category else top_k)

        # Filter by category if specified
        if category:
            results = [r for r in results if r.category.lower() == category.lower()]
            results = results[:top_k]

        return results

    def get_categories(self) -> List[str]:
        """Get all categories in the knowledge base"""
        if not self._indexed:
            self.index_knowledge_base()

        categories = set()
        if isinstance(self.engine, SemanticSearchEngine):
            for doc in self.engine.documents.values():
                categories.add(doc.category)
        elif isinstance(self.engine, KeywordSearchEngine):
            for doc in self.engine.documents.values():
                categories.add(doc.category)

        return sorted(list(categories))

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get a specific document by ID"""
        if isinstance(self.engine, SemanticSearchEngine):
            return self.engine.documents.get(doc_id)
        elif isinstance(self.engine, KeywordSearchEngine):
            return self.engine.documents.get(doc_id)
        return None


# Convenience function
def create_searcher(knowledge_base_path: str = "knowledge_base",
                   use_semantic: bool = True) -> KnowledgeBaseSearcher:
    """
    Create and initialize a knowledge base searcher

    Args:
        knowledge_base_path: Path to knowledge base
        use_semantic: Whether to use semantic search

    Returns:
        Initialized KnowledgeBaseSearcher
    """
    searcher = KnowledgeBaseSearcher(
        knowledge_base_path=knowledge_base_path,
        use_semantic=use_semantic
    )
    searcher.index_knowledge_base()
    return searcher


if __name__ == "__main__":
    # Example usage
    import sys

    kb_path = sys.argv[1] if len(sys.argv) > 1 else "knowledge_base"

    print(f"Initializing knowledge base searcher...")
    searcher = create_searcher(kb_path)

    print(f"\nCategories: {searcher.get_categories()}")

    # Interactive search
    while True:
        query = input("\nEnter search query (or 'quit'): ").strip()
        if query.lower() in ('quit', 'exit', 'q'):
            break

        results = searcher.search(query, top_k=5)

        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.title} (score: {result.score:.3f})")
            print(f"   Category: {result.category}")
            print(f"   {result.snippet}")
