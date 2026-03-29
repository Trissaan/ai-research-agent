# 🤖 AI Research Agent

A multi-agent research system built from scratch using the Anthropic SDK. No frameworks — just raw Python and the ReAct pattern.

## What It Does

Give it a question, and it autonomously researches the topic by looping through:

1. **Reason** — Claude thinks about what it needs to find out
2. **Act** — Calls a tool (search, summarize, etc.)
3. **Observe** — Reads the result and decides what to do next
4. **Repeat** — Until it has enough info to give a solid answer

```
🤖 AGENT STARTING — Question: What are AI agents?

── Loop 1 ──
  💭 Claude thinks: Let me search for general info about AI agents...
  🔧 Claude calls: search({"query": "AI agents 2025"})

── Loop 2 ──
  💭 Claude thinks: Now let me find business use cases...
  🔧 Claude calls: search({"query": "enterprise AI agent adoption"})

...

✅ AGENT FINISHED after 7 loops
```

## Architecture

```
User Question
     │
     ▼
┌──────────┐
│  REASON  │ ← Claude decides what to do next
└────┬─────┘
     │
┌────▼─────┐
│   ACT    │ ← Calls search() or summarize()
└────┬─────┘
     │
┌────▼─────┐
│ OBSERVE  │ ← Result fed back into conversation
└────┬─────┘
     │
     ▼
  Loop again? ──Yes──▶ Back to REASON
     │
     No
     │
     ▼
  Final Answer
```

## Concepts Covered

- **ReAct Loop** — Reason → Act → Observe → Repeat
- **Tool Use** — Claude calls Python functions via the Anthropic tools API
- **Prompt Engineering** — System prompts that guide agent behaviour
- **Structured Outputs** — Parsing tool call responses as structured data

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-research-agent.git
cd ai-research-agent

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo ANTHROPIC_API_KEY=your-key-here > .env

# Run the agent
python agent.py
```

## Build Log

| Day | What I Built |
|-----|-------------|
| 1   | ReAct agent loop with dummy tools |
| 2   | *Coming soon — real web search + scraping* |
| 3   | *Coming soon — RAG + embeddings* |
| 4   | *Coming soon — memory + MCP* |
| 5   | *Coming soon — multi-agent system* |
| 6   | *Coming soon — UI + deployment* |
| 7   | *Coming soon — outreach* |

## Stack

- **LLM:** Claude (Anthropic SDK)
- **Language:** Python
- **Pattern:** ReAct (no frameworks)

---

*Built in 7 days as a hands-on deep dive into every major gen AI concept.*