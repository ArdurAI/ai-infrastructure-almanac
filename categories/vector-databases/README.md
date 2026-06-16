# Vector Databases & RAG Infrastructure

Market: $2.65B (2025) → $8.44B (2030) at 23-27.5% CAGR. 25+ distinct vector databases actively maintained. The "Postgres vs. dedicated vector DB" debate is the central infrastructure fork. **Document parsing is the #1 RAG quality bottleneck.**

## The Roster

| Tier | Tools |
|------|-------|
| **A** | Pinecone, Qdrant, Weaviate, Milvus, Chroma, pgvector, Zilliz / Vector Lakebase, Turbopuffer, Vorkath, LanceDB, Elasticsearch / ESRE, OpenSearch, Redis Vector, FAISS, ScaNN, LangChain / LangGraph, LlamaIndex, Haystack, Ragas, TruLens, DeepEval, Braintrust, LangSmith, Firecrawl, LlamaParse, Unstructured, Docling (IBM), Cohere Rerank, Voyage AI Rerank, Glean, Microsoft Copilot / M365 |
| **B** | MongoDB Atlas Vector Search, SingleStore, DataStax Astra (Cassandra), Marqo, ClickHouse, DuckDB, Oracle AI Database 26ai, Apache Cassandra 5.0, Vald, Cloudflare Vectorize, Turso / sqlite-vec, Vespa, HNSWlib, DiskANN, USearch, ZeroEntropy zerank-1, BGE Reranker v2, Jina AI Rerank, Reducto, LandingAI ADE, Mistral OCR 3, Marker-PDF, AWS Textract, Google Document AI, Azure Document Intelligence, Docsumo, Onyx (Danswer), SphereIQ, PipesHub, Guru, GoSearch, Coveo, Algolia, Meilisearch, Typesense, Neo4j, Amazon Neptune, ArangoDB, Actian VectorAI DB, KDB.AI, Deep Lake (Activeloop), Ollama, vLLM, Pinecone Nexus, Chroma Context-1, Weaviate Engram |
| **C** | pdfmux, MinerU / MinerU-Popo, Vectorize AI |

## Key Trends

- **Hybrid search is now default**: Pure vector retrieval is a starting point; production RAG requires BM25 + dense + reranking.
- **Agentic RAG shift**: Vector DBs evolving from passive retrieval to active knowledge engines — Pinecone Nexus, Chroma Context-1, Weaviate Engram.
- **Cost tipping point at 60-80M queries/month**: Self-hosted Qdrant/Weaviate undercuts Pinecone Serverless by 3-10x above this threshold.
- **New indexing algorithms**: ACORN (Qdrant), RaBitQ (FAISS), SOAR (ScaNN), DiskANN, Vortex (Zilliz) pushing beyond basic HNSW.
- **Parser quality is the #1 bottleneck**: VLM-based parsers (Mistral OCR 3, LlamaParse agentic mode) displacing classic OCR.

## Benchmarks

- **Standard**: ANN-Benchmarks, BEIR, MS MARCO
- **Custom**: Setup time, index build time, query latency at scale, memory footprint
- **Stress**: Concurrent ingestion + query, index corruption, node failure, parser accuracy on complex documents

## See also

- Full catalog: [`../data/roster.json`](../data/roster.json)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
- Benchmark methodology: [`../methodology/benchmark-harness.md`](../methodology/benchmark-harness.md)
