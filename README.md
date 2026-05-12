# 🧠 Nexus AI: The Enterprise Brain

Nexus AI là một hệ thống Agentic API trung tâm, được thiết kế để trở thành "bộ não" của doanh nghiệp. Hệ thống không chỉ trả lời câu hỏi mà còn có khả năng ghi nhớ, truy vấn tri thức nội bộ và thực thi các tác vụ hỗ trợ IT/Vận hành.

---

## 🏗️ Project Structure

```text
project-root/
│
├── app/
│   ├── api/                    # 1. API LAYER (FastAPI)
│   │   ├── dependencies.py     # Auth, Rate limiting, Inject DB/LLM sessions
│   │   ├── routers/            # Các Endpoints
│   │   │   ├── chat.py         # Streaming endpoints cho Agent
│   │   │   ├── documents.py    # Upload file để đưa vào Vector DB (cho RAG)
│   │   │   └── webhooks.py     # Nhận callback từ các tools bất đồng bộ
│   │   └── schemas/            # Pydantic models cho Request/Response
│   │
│   ├── agents/                 # 2. AGENTIC LAYER (LangGraph)
│   │   ├── graphs/             # Định nghĩa luồng (Workflows)
│   │   │   ├── supervisor.py   # Multi-agent: Router phân việc cho các agent con
│   │   │   └── worker.py       # Các sub-graph xử lý task cụ thể (Code, Research)
│   │   ├── nodes/              # Logic từng bước (Reasoning, Calling Tool, Formatting)
│   │   ├── state.py            # TypedDict / Pydantic quy định State của đồ thị
│   │   └── prompts/            # Chứa các System Prompts, Few-shot templates
│   │
│   ├── rag/                    # 3. RAG LAYER (Retrieval-Augmented Generation)
│   │   ├── ingestion/          # Đọc dữ liệu (PDF, Web Scraping, Notion API)
│   │   ├── processing/         # Text Splitters, Chunking strategies
│   │   ├── embeddings.py       # Khởi tạo mô hình Embedding (OpenAI, HuggingFace)
│   │   └── retrievers/         # Logic tìm kiếm (Vector Search, Hybrid Search, Keyword)
│   │
│   ├── mcp/                    # 4. MCP LAYER (Model Context Protocol)
│   │   ├── clients/            # Kết nối với các MCP Servers bên ngoài (Github, Slack, Google Drive)
│   │   ├── servers/            # Expose service nội bộ của bạn thành 1 MCP Server
│   │   └── registry.py         # Quản lý danh sách các Resources và Prompts từ MCP
│   │
│   ├── tools/                  # 5. NATIVE TOOLS LAYER (Công cụ truyền thống)
│   │   ├── definitions/        # Định nghĩa Pydantic args schema cho tools
│   │   ├── search_tool.py      # Ví dụ: Tavily, DuckDuckGo
│   │   ├── executor.py         # Sandbox để chạy Python code an toàn
│   │   └── custom_api.py       # API nội bộ doanh nghiệp
│   │
│   ├── core/                   # 6. CORE & CONFIG LAYER
│   │   ├── config.py           # pydantic-settings load .env (API Keys, DB URIs)
│   │   ├── llm_factory.py      # Khởi tạo mô hình (GPT-4, Claude 3.5, Gemini)
│   │   ├── security.py         # Xử lý JWT, CORS
│   │   └── observability.py    # Cấu hình Tracing (LangSmith, OpenTelemetry)
│   │
│   ├── database/               # 7. PERSISTENCE LAYER
│   │   ├── relational/         # PostgreSQL/MySQL (Lưu user, meta-data)
│   │   │   └── models.py       # SQLAlchemy/SQLModel models
│   │   ├── vector_db/          # Milvus, Qdrant, Pinecone (Lưu Vectors cho RAG)
│   │   └── checkpointers/      # PostgresSaver / RedisSaver để lưu State của LangGraph
│   │
│   └── services/               # 8. BUSINESS LOGIC (Không liên quan đến LLM)
│       └── billing_service.py  # Ví dụ: Tính phí token người dùng
│
├── tests/                      # 9. TESTING & EVALUATION
│   ├── unit/                   # Test các functions cơ bản
│   ├── integration/            # Test API flow
│   └── evaluation/             # Đánh giá chất lượng RAG/Agent (bằng Ragas, TruLens)
│
├── scripts/                    # Script chạy cronjob, migrate DB, test tool
├── docker/                     # Dockerfile, docker-compose.yml (App, DB, Redis)
├── .env.example
├── pyproject.toml              # Quản lý thư viện (Poetry/Pipenv)
└── README.md
```

---

## 🚀 Scaling Roadmap (Sprint-based)

### 🏃 Sprint 1: Foundation & External Awareness
- **Mục tiêu:** Dựng khung API và Agent có khả năng tra cứu Internet.
- **Task:** 
    - Setup FastAPI + LangGraph basic graph.
    - Implement `tools/search.py` dùng `ddgs`.
    - Streaming chat endpoint.

### 🏃 Sprint 2: The Knowledgeable Brain (RAG)
- **Mục tiêu:** Agent có thể trả lời dựa trên tài liệu nội bộ.
- **Task:**
    - Implement `api/documents.py` (Upload PDF).
    - Setup Vector Database (ChromaDB hoặc FAISS).
    - Viết `tools/document_rag.py` để Agent tự tìm kiến thức trong kho PDF.

### 🏃 Sprint 3: The Persistent Memory
- **Mục tiêu:** Agent nhớ được ngữ cảnh và thông tin người dùng qua nhiều phiên chat.
- **Task:**
    - Tích hợp LangGraph Checkpointers (SQLite hoặc Postgres).
    - Quản lý `thread_id` để phân tách hội thoại của từng nhân viên.

### 🏃 Sprint 4: The Agentic Workforce (Multi-Agent)
- **Mục tiêu:** Chia tách trách nhiệm cho các Agent chuyên biệt.
- **Task:**
    - Xây dựng `supervisor.py` để điều phối.
    - Tạo `IT Worker` (chuyên troubleshoot) và `HR Worker` (chuyên chính sách).

### 🏃 Sprint 5: Action & Integration (MCP)
- **Mục tiêu:** Agent thực thi tác vụ trên các công cụ doanh nghiệp.
- **Task:**
    - Tích hợp MCP Servers cho Slack (gửi thông báo) và Jira (tạo task).
    - Implement `webhooks.py` để nhận cảnh báo từ hệ thống.

### 🏃 Sprint 6: Enterprise Hardening
- **Mục tiêu:** Đưa hệ thống lên môi trường sản xuất (Production-ready).
- **Task:**
    - Implement Auth (OAuth2/JWT).
    - Setup Docker & Monitoring (LangSmith).
    - Viết Test case tự động cho toàn bộ Pipeline.

---

## 🛠️ Installation & Setup

1. **Clone repository:**
   ```bash
   git clone <repo-url>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables:**
   Copy `.env.example` thành `.env` và điền các API Keys cần thiết.
4. **Run Server:**
   ```bash
   uvicorn app.api.main:app --reload
   ```