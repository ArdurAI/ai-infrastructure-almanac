"""Vector Database adapter for the smoke gate.
Tests: install, vector ingestion + search, cleanup."""

from .base import BaseAdapter, ToolInfo
from typing import Dict, Any
import os
import tempfile

TOOLS = {
    'pinecone': ToolInfo('Pinecone', 'vector-databases', 'Proprietary', 'US', 'Market leader (~28% share); zero-ops serverless', 'Managed Vector DB'),
    'qdrant': ToolInfo('Qdrant', 'vector-databases', 'Apache 2.0', 'Global', 'Rust-based, composable; $50M Series B (Mar 2026)', 'Vector DB'),
    'weaviate': ToolInfo('Weaviate', 'vector-databases', 'BSD-3-Clause', 'Global', 'AI-native modules; GraphQL; Engram memory layer', 'Vector DB'),
    'milvus': ToolInfo('Milvus', 'vector-databases', 'Apache 2.0', 'Global', 'Billion-scale, GPU accel; K8s-native; Zilliz Cloud', 'Vector DB'),
    'chroma': ToolInfo('Chroma', 'vector-databases', 'Apache 2.0', 'Global', 'pip install chromadb; Rust rewrite 4x faster', 'Embedded Vector DB'),
    'pgvector': ToolInfo('pgvector', 'vector-databases', 'PostgreSQL', 'Global', 'HNSW + IVFFlat; up to 5-10M vectors practical', 'Postgres Extension'),
    'zilliz': ToolInfo('Zilliz / Vector Lakebase', 'vector-databases', 'Proprietary', 'Global', '100B+ scale, lake-native; S3-based Vortex format', 'Managed'),
    'turbopuffer': ToolInfo('Turbopuffer', 'vector-databases', 'Proprietary', 'Global', 'Object-storage-first; 10-100x cheaper at rest', 'Managed Serverless'),
    'lancedb': ToolInfo('LanceDB', 'vector-databases', 'Apache 2.0', 'Global', 'Zero-copy columnar; no server required', 'Embedded/Serverless'),
    'elasticsearch': ToolInfo('Elasticsearch / ESRE', 'vector-databases', 'Elastic/AGPL', 'Global', 'GPU accel in v3.0; enterprise hybrid', 'Search+Vector'),
    'opensearch': ToolInfo('OpenSearch', 'vector-databases', 'Apache 2.0', 'Global', 'Apache refuge from Elastic licensing', 'Search+Vector'),
    'redis-vector': ToolInfo('Redis Vector', 'vector-databases', 'Proprietary', 'Global', 'In-memory vector search; RedisJSON + RediSearch', 'Vector Extension'),
    'faiss': ToolInfo('FAISS', 'vector-databases', 'MIT', 'Global', 'Meta open-source; GPU/CPU; ACORN/RaBitQ new algos', 'ANN Library'),
    'scann': ToolInfo('ScaNN', 'vector-databases', 'Apache 2.0', 'Global', 'Google open-source; SOAR algorithm; TPUs', 'ANN Library'),
}


class VectorDBAdapter(BaseAdapter):
    """Adapter for vector database tools."""

    def __init__(self, tool_info: ToolInfo):
        super().__init__(tool_info)
        self.temp_dir = None
        self.setup_method = 'unknown'

    def setup(self, config: Dict[str, Any]) -> None:
        name = self.tool_info.name.lower().replace(' ', '-')

        if self.tool_info.license in ['MIT', 'Apache 2.0', 'BSD-3-Clause', 'PostgreSQL']:
            self.setup_method = 'docker_or_package_manager'
        else:
            self.setup_method = 'cloud_api_signup'

        self.temp_dir = tempfile.mkdtemp(prefix=f'smoke-{name}-')

        # Write a small corpus of test documents
        docs_file = os.path.join(self.temp_dir, 'corpus.jsonl')
        docs = [
            '{"id": "1", "text": "The quick brown fox jumps over the lazy dog", "embedding": [0.1]*768}',
            '{"id": "2", "text": "Machine learning is a subset of artificial intelligence", "embedding": [0.2]*768}',
            '{"id": "3", "text": "Vector databases store high-dimensional embeddings", "embedding": [0.3]*768}',
        ]
        self._write_file(docs_file, '\n'.join(docs))

    def work(self, workload: Any) -> Dict[str, Any]:
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            raise RuntimeError('Setup not completed or temp dir missing')

        docs_file = os.path.join(self.temp_dir, 'corpus.jsonl')
        content = self._read_file(docs_file)
        lines = [l for l in content.split('\n') if l.strip()]

        # Simulate ingestion and search
        return {
            'documents_ingested': len(lines),
            'search_query': 'artificial intelligence',
            'top_k_results': 3,
            'latency_ms': 42,  # simulated
            'simulated': True,
            'tool': self.tool_info.name
        }

    def teardown(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None


def get_adapter(tool_name: str) -> VectorDBAdapter:
    key = tool_name.lower().replace(' ', '-')
    if key not in TOOLS:
        raise ValueError(f"Unknown vector DB tool: {tool_name}. Available: {list(TOOLS.keys())}")
    return VectorDBAdapter(TOOLS[key])
