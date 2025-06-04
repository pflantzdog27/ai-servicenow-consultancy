# AI-Powered ServiceNow Consultancy Platform

An AI-powered platform that automates ServiceNow consulting services using multi-agent orchestration, reducing assessment time from weeks to hours.

## Features

- 🤖 6 Specialized AI Agents (Discovery, Architecture, Configuration, Documentation, Analysis, Project Management)
- ⚡ 4x faster assessments (1 week vs 4 weeks traditional)
- 💰 50% cost reduction through AI automation
- 🔒 SOC2-ready security architecture
- 📊 Real-time monitoring dashboard
- 🎯 Tiered pricing (Starter/Professional/Enterprise)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+
- API Keys: OpenAI, Anthropic (optional: Pinecone)

### Setup

1. Clone the repository:
\`\`\`bash
git clone https://github.com/YOUR-USERNAME/ai-servicenow-consultancy.git
cd ai-servicenow-consultancy
\`\`\`

2. Copy environment file and add your API keys:
\`\`\`bash
cp .env.example .env
# Edit .env with your API keys
\`\`\`

3. Run with Docker Compose:
\`\`\`bash
docker-compose up
\`\`\`

4. Access the platform:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Architecture

- **Backend**: Python/FastAPI with LangGraph orchestration
- **Frontend**: React/Next.js with real-time updates  
- **Database**: PostgreSQL + Redis
- **AI Models**: GPT-4, Claude, Llama (configurable)

## Development

\`\`\`bash
# Run tests
make test

# Development mode
make dev

# View logs
docker-compose logs -f
\`\`\`

## License

MIT