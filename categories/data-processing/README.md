# Data Processing

> **Cross-cutting concern.** Data processing, document parsing, and embedding tools are currently tracked within the [Vector Databases & RAG Infrastructure](../vector-databases/) category, as they are the upstream pipeline that feeds retrieval systems. This dedicated directory will be populated if the category grows large enough to warrant a split in a future edition.

## Key Tools (in Vector Databases)

| Tool | Type | Focus |
|------|------|-------|
| Firecrawl | Document Parsing | API-first web+PDF → Markdown; Rust-based PDF engine |
| LlamaParse | Document Parsing | Agentic OCR for RAG; 90+ formats |
| Unstructured | Document Parsing | 25+ format semantic extraction; element-typed output |
| Docling (IBM) | Layout Parser | 61K stars; open-source layout parser; MCP server |
| Reducto | Document Parsing | Agentic OCR correction; ~20% higher accuracy |
| LandingAI ADE | Document Parsing | Regulated industries; visual grounding; DPT-2 |
| Mistral OCR 3 | Document Parsing | VLM-based document understanding |
| Marker-PDF | Document Parsing | GPU-accelerated layout-perfect Markdown |
| pdfmux | Document Parsing | Self-hosted; confidence-scored; CPU-only |
| MinerU / MinerU-Popo | Document Parsing | Post-processing OCR for cross-page continuity |
| AWS Textract | Document Parsing | AWS ecosystem; enterprise OCR at scale |
| Google Document AI | Document Parsing | GCP ecosystem; 200+ languages, handwriting |
| Azure Document Intelligence | Document Parsing | Azure ecosystem; enterprise compliance |
| Docsumo | Document Parsing | Finance/ops; no-code document workflows |
| Cohere Rerank | Reranker | Cross-encoder reranking; rerank-v3.5; multilingual |
| Voyage AI Rerank | Reranker | Instruction-following; rerank-2.5; agent/conversation tuned |
| ZeroEntropy zerank-1 | Reranker | Fastest latency; 60ms; 0.89 NDCG@10 healthcare |
| BGE Reranker v2 | Reranker | Open-source; Chinese+English; cross-encoder |
| Jina AI Rerank | Reranker | Open-weight; multimodal; images + PDFs; late chunking |
| Vectorize AI | RAG Data Prep | Seed stage ($3.6M); unstructured → vector DB optimization |

## See also

- Full vector DB catalog: [`../vector-databases/README.md`](../vector-databases/README.md)
- Latest edition: [`../editions/2026-06.md`](../editions/2026-06.md)
