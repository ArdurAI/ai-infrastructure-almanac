# Vector Databases — Testing Methodology

How we test and score vector databases, ANN libraries, and document parsing tools in the almanac.

## Scope

This category covers vector stores, approximate nearest neighbor (ANN) libraries, RAG frameworks, and document parsing pipelines.

## Adapter pattern

```python
class VectorDBAdapter(CategoryAdapter):
    def setup(self, config) -> None:
        # Start the DB (docker run or cloud connect), create index
        pass
    
    def load(self, documents) -> None:
        # Ingest documents with embeddings, wait for index readiness
        pass
    
    def query(self, query) -> Response:
        # Run vector search + optional hybrid search, return top-k results
        pass
    
    def teardown(self) -> None:
        # Delete index, stop container, clean data
        pass
```

## Standard benchmarks

### 1. ANN Benchmarks (erikbern/ann-benchmarks)
- **What**: Standardized nearest-neighbor search on datasets like GloVe, SIFT, DeepImage
- **Why**: Widely accepted comparison of recall vs. latency tradeoffs
- **Metric**: Recall@100 vs. QPS (queries per second), index build time

### 2. BEIR (Benchmarking IR)
- **What**: 18 information retrieval datasets for zero-shot evaluation
- **Why**: Tests RAG retrieval quality in realistic settings
- **Metric**: NDCG@10, MAP, Recall@100

### 3. DocParsing Benchmark (Custom)
- **What**: 100 documents (PDF, DOCX, HTML, images) with ground-truth structured output
- **Why**: Document parsing is the #1 RAG bottleneck
- **Metric**: Structure accuracy, text extraction completeness, table preservation

## Custom PlatformOps benchmarks

### Ingestion throughput
- **Tasks**: Ingest 1K, 100K, 1M, 10M vectors (768-dim, 1536-dim)
- **Metrics**: Vectors/second, memory growth, disk usage, index build time

### Query latency at scale
- **Tasks**: Query with 1, 10, 100, 1000 concurrent clients
- **Metrics**: P50, P95, P99 latency, QPS, error rate

### Hybrid search quality
- **Tasks**: Run queries with vector + BM25 + reranking combinations
- **Metrics**: NDCG improvement vs. pure vector, latency overhead

### Filtered search
- **Tasks**: Vector search with metadata filters (e.g., `date > 2024 AND category = 'tech'`)
- **Metrics**: Latency impact of filters, result accuracy under filtering

### Document parsing pipeline
- **Tasks**: Parse 100 documents through each parser, feed to RAG pipeline
- **Metrics**: End-to-end RAG accuracy, parser latency, format support

## Scoring dimensions

| Dimension | Weight | How measured |
|-----------|--------|-------------|
| **Accuracy** | 25% | ANN recall@100, BEIR NDCG@10, RAG end-to-end accuracy |
| **Latency** | 15% | Query P99 latency, index build time, ingestion rate |
| **Token economics** | 10% | Storage cost per million vectors, compute cost at query time |
| **Scale behavior** | 15% | Performance at 1M, 10M, 100M vectors; concurrent query handling |
| **Ops burden** | 15% | Deployment complexity, monitoring, backup/restore, upgrade path |
| **Developer experience** | 15% | SDK quality, documentation, query language ergonomics |
| **Data sovereignty** | 5% | Self-host option, on-premise deployment, data export |

## Stress suites

### Contradiction storm
- Documents with contradictory information on the same topic
- Measure: Does retrieval surface the contradiction? Which version is returned?

### Near-duplicate flood
- 100K documents where 90% are near-duplicates
- Measure: Deduplication quality, storage efficiency, query accuracy

### Temporal paradox
- Update documents with new versions, query old vs. new
- Measure: Version handling, consistency, stale data detection

### Concurrent writers
- 100 clients writing vectors simultaneously
- Measure: Write throughput, lock contention, data integrity

### Kill-the-backing-store
- Kill the storage backend (disk, S3, etc.) mid-query
- Measure: Graceful degradation, query retry, data loss

## Known pitfalls

1. **Embedding model dependency**: Retrieval quality depends heavily on the embedding model. We fix the model (text-embedding-3-large) across all tests.
2. **Index warmup**: Some DBs have cold-start penalties. We allow warm-up before timing.
3. **Dimension sensitivity**: Results vary by vector dimension. We test 768 and 1536.
4. **Filtering interaction**: Filtered vector search can be 10x slower than pure vector. We test both.

## License
Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / AI Infrastructure Almanac**.
