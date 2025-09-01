import os
import glob
from pypdf import PdfReader
from bs4 import BeautifulSoup
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import sqlite3
import hashlib
import re
from pathlib import Path
from datetime import datetime
import json

KNOWLEDGE_BASE_DIR = 'disaster_knowledge_base'
VECTOR_STORE_PATH = 'vector_store'
KNOWLEDGE_DB_PATH = 'preparedness_data/knowledge_base.db'

def _init_knowledge_db():
    """Initialize database for knowledge base indexing"""
    conn = sqlite3.connect(KNOWLEDGE_DB_PATH)
    cursor = conn.cursor()
    
    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            file_name TEXT,
            category TEXT,
            title TEXT,
            content TEXT,
            content_hash TEXT,
            file_type TEXT,
            last_indexed TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            section_title TEXT,
            section_content TEXT,
            section_level INTEGER,
            section_order INTEGER,
            FOREIGN KEY (document_id) REFERENCES knowledge_documents (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT,
            document_id INTEGER,
            section_id INTEGER,
            frequency INTEGER,
            positions TEXT,
            FOREIGN KEY (document_id) REFERENCES knowledge_documents (id),
            FOREIGN KEY (section_id) REFERENCES knowledge_sections (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactive_checklists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            checklist_title TEXT,
            items TEXT,
            category TEXT,
            priority INTEGER,
            FOREIGN KEY (document_id) REFERENCES knowledge_documents (id)
        )
    ''')
    
    # Create indexes for faster searching
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_term ON search_index (term)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_doc ON search_index (document_id)')
    
    conn.commit()
    conn.close()

def _tokenize(text: str) -> list[str]:
    """Tokenize text for indexing, including bigrams."""
    tokens = re.findall(r'\b[a-z]+\b', text.lower())
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    filtered_tokens = [t for t in tokens if t not in stop_words and len(t) > 2]

    # Add bigrams
    bigrams = []
    for i in range(len(filtered_tokens) - 1):
        bigrams.append(f"{filtered_tokens[i]} {filtered_tokens[i+1]}")

    print(f"DEBUG: Tokenized text: {filtered_tokens + bigrams}") # DEBUG
    return filtered_tokens + bigrams

def _index_content(cursor, doc_id: int, section_id: int, content: str):
    """Index content for search"""
    tokens = _tokenize(content)
    
    term_freq = {}
    for i, token in enumerate(tokens):
        if token not in term_freq:
            term_freq[token] = {'count': 0, 'positions': []}
        term_freq[token]['count'] += 1
        term_freq[token]['positions'].append(i)
    
    for term, data in term_freq.items():
        print(f"DEBUG: Indexing term: {term}, data: {data}") # DEBUG
        cursor.execute('''
            INSERT INTO search_index (term, document_id, section_id, frequency, positions)
            VALUES (?, ?, ?, ?, ?)
        ''', (term, doc_id, section_id, data['count'], json.dumps(data['positions'])))

def _extract_title(content: str, file_path_stem: str) -> str:
    """Extract title from markdown content or use filename"""
    lines = content.split('\n')
    for line in lines[:10]:
        if line.startswith('# '):
            return line[2:].strip()
    return file_path_stem.replace('_', ' ').title()

def _extract_sections(content: str) -> list[dict]:
    """Extract sections from markdown content"""
    sections = []
    current_section = {'title': 'Introduction', 'content': '', 'level': 0}
    
    for line in content.split('\n'):
        if line.startswith('#'):
            if current_section['content'].strip():
                sections.append(current_section)
            
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            current_section = {'title': title, 'content': '', 'level': level}
        else:
            current_section['content'] += line + '\n'
    
    if current_section['content'].strip():
        sections.append(current_section)
    
    return sections

def _determine_category(file_path: str, content: str) -> str:
    """Determine category from file path and content"""
    path_lower = file_path.lower()
    content_lower = content.lower()[:1000]
    
    categories = {
        "water": ["water", "hydration", "purification", "filter", "boil", "distill", "rain", "collection"],
        "food": ["food", "nutrition", "cooking", "preservation", "storage", "foraging", "hunting", "calories"],
        "shelter": ["shelter", "housing", "warmth", "insulation", "construction", "building", "protection"],
        "medical": ["medical", "first aid", "injury", "medicine", "health", "wound", "emergency care", "pain"],
        "power": ["power", "electricity", "generator", "solar", "battery", "energy", "lighting", "fuel"],
        "communication": ["communication", "radio", "phone", "internet", "signal", "emergency broadcast"],
        "security": ["security", "defense", "protection", "safety", "perimeter", "locks", "surveillance"],
        "sanitation": ["sanitation", "hygiene", "waste", "toilet", "cleaning", "disposal", "disease"],
        "psychology": ["psychology", "mental", "stress", "community", "morale", "panic", "leadership"],
        "evacuation": ["evacuation", "bug out", "escape", "route", "transportation", "assembly"]
    }

    for category in categories:
        if category in path_lower:
            return category
    
    best_category = "general"
    best_score = 0
    
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in content_lower)
        if score > best_score:
            best_score = score
            best_category = category
    
    return best_category

def build_vector_store():
    """
    Reads all .md and .pdf files, creates chunks with metadata, and saves them to a FAISS vector store.
    Also populates the knowledge_base.db for search functionality.
    """
    _init_knowledge_db()
    conn_kb = sqlite3.connect(KNOWLEDGE_DB_PATH)
    cursor_kb = conn_kb.cursor()

    docs = []
    print(f"Building vector store from files in {KNOWLEDGE_BASE_DIR}...")

    file_paths = glob.glob(os.path.join(KNOWLEDGE_BASE_DIR, '**', '*.md'), recursive=True)
    file_paths.extend(glob.glob(os.path.join(KNOWLEDGE_BASE_DIR, '**', '*.pdf'), recursive=True))

    for file_path_str in file_paths:
        file_path = Path(file_path_str)
        content = ''
        file_type = ''

        if file_path.suffix == ".pdf":
            file_type = 'pdf'
            try:
                reader = PdfReader(file_path_str)
                for page in reader.pages:
                    content += page.extract_text() or ''
            except Exception as e:
                print(f"Could not read {file_path_str} as PDF: {e}. Trying to read as HTML.")
                file_type = 'html'
                try:
                    with open(file_path_str, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    content = soup.get_text()
                except Exception as e2:
                    print(f"Could not read {file_path_str} as HTML: {e2}")
                    continue
        elif file_path.suffix == ".md":
            file_type = 'markdown'
            with open(file_path_str, 'r', encoding='utf-8') as f:
                content = f.read()
        
        if content:
            # Populate knowledge_base.db
            full_path = str(file_path)
            content_hash = hashlib.md5(content.encode()).hexdigest()
            category = _determine_category(full_path, content)
            title = _extract_title(content, file_path.stem)

            cursor_kb.execute('''
                INSERT OR REPLACE INTO knowledge_documents 
                (file_path, file_name, category, title, content, content_hash, file_type, last_indexed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (full_path, file_path.name, category, title, content, content_hash, 
                  file_type, datetime.now().isoformat()))
            
            doc_id = cursor_kb.lastrowid
            if doc_id == 0: # If it was an REPLACE, get the existing ID
                cursor_kb.execute("SELECT id FROM knowledge_documents WHERE file_path = ?", (full_path,))
                doc_id = cursor_kb.fetchone()[0]

            sections = _extract_sections(content)
            for i, section in enumerate(sections):
                cursor_kb.execute('''
                    INSERT INTO knowledge_sections 
                    (document_id, section_title, section_content, section_level, section_order)
                    VALUES (?, ?, ?, ?, ?)
                ''', (doc_id, section['title'], section['content'], section['level'], i))
                
                section_id = cursor_kb.lastrowid
                _index_content(cursor_kb, doc_id, section_id, section['content'])

            # Add to docs for FAISS vector store
            docs.append(Document(page_content=content, metadata={"source": file_path_str, "title": title, "category": category}))
            conn_kb.commit() # Commit after each document is processed

    conn_kb.close()

    print(f"Found and processed {len(docs)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunked_docs = text_splitter.split_documents(docs)

    print(f"Created {len(chunked_docs)} text chunks.")

    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    print("Creating and saving vector store...")
    vector_store = FAISS.from_documents(chunked_docs, embedding=embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"Vector store built successfully and saved to {VECTOR_STORE_PATH}")

if __name__ == '__main__':
    build_vector_store()
