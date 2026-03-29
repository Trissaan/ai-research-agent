"""
🤖 DAY 1 — Your First ReAct Agent
===================================

WHAT IS A ReAct LOOP?
Think of how YOU research something:
  1. You THINK about what you need to find out        (Reason)
  2. You SEARCH Google or ask someone                 (Act)
  3. You READ the result and decide what to do next   (Observe)
  4. Repeat until you have a good answer

A ReAct agent does the exact same thing, but it's an AI doing
the thinking, searching, and reading — in a loop.

    ┌──────────┐
    │  REASON  │ ← Claude thinks: "I should search for X"
    └────┬─────┘
         │
    ┌────▼─────┐
    │   ACT    │ ← Claude calls a tool: search("X")
    └────┬─────┘
         │
    ┌────▼─────┐
    │ OBSERVE  │ ← We run the tool, give Claude the result
    └────┬─────┘
         │
         │  Not done yet? Loop back to REASON
         │  Done? Give final answer
         ▼

HOW TO RUN THIS:
  1. Install the SDK:   pip install anthropic
  2. Set your API key:  export ANTHROPIC_API_KEY="sk-ant-..."
     (Get your key from https://console.anthropic.com)
  3. Run it:            python agent.py
"""

import anthropic
import json
from dotenv import load_dotenv
load_dotenv()


# ─────────────────────────────────────────────
# STEP 1: Define your dummy tools
# ─────────────────────────────────────────────
# These are FAKE tools for now. They return hardcoded results.
# On Day 2, you'll replace these with real web search + scraping.
# The point today is to get the LOOP working.

def search(query: str) -> str:
    """Pretend to search the web. Returns fake results."""
    print(f"  🔍 [TOOL] Searching for: {query}")
    
    # Fake results — just enough to give the agent something to work with
    fake_results = {
        "default": [
            {"title": "AI Agents in 2025 — Overview", "snippet": "AI agents are autonomous systems that use LLMs to reason, plan, and take actions. Key frameworks include LangChain, CrewAI, and custom ReAct loops."},
            {"title": "Building Your First Agent", "snippet": "The simplest agent pattern is ReAct: Reason, Act, Observe. Give an LLM tools and let it decide when to use them."},
            {"title": "Enterprise AI Adoption", "snippet": "72% of enterprises plan to deploy AI agents by 2026. Common use cases include research automation, customer support, and data analysis."},
        ]
    }
    return json.dumps(fake_results["default"], indent=2)


def summarize(text: str) -> str:
    """Pretend to summarize text. Returns a condensed version."""
    print(f"  📝 [TOOL] Summarizing {len(text)} characters of text...")
    
    # In reality, you might call Claude again here with a summarization prompt.
    # For now, just return a fake summary.
    return "Summary: AI agents use LLMs in a loop of reasoning and tool use. Key patterns include ReAct. Adoption is growing fast, with 72% of enterprises planning deployment by 2026."


# ─────────────────────────────────────────────
# STEP 2: Describe tools for Claude
# ─────────────────────────────────────────────
# Claude needs to know what tools it CAN call.
# We describe them in this specific format so Claude
# understands the name, purpose, and parameters of each tool.

tools = [
    {
        "name": "search",
        "description": "Search the web for information on a topic. Use this to find facts, recent developments, or background info.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "summarize",
        "description": "Summarize a long piece of text into key points. Use this after gathering enough raw information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to summarize"
                }
            },
            "required": ["text"]
        }
    }
]


# ─────────────────────────────────────────────
# STEP 3: Run a tool when Claude asks for one
# ─────────────────────────────────────────────
# When Claude decides to use a tool, it sends back a "tool_use"
# block with the tool name and inputs. We catch that here and
# run the matching Python function.

def run_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool and return the result as a string."""
    if tool_name == "search":
        return search(tool_input["query"])
    elif tool_name == "summarize":
        return summarize(tool_input["text"])
    else:
        return f"Error: Unknown tool '{tool_name}'"


# ─────────────────────────────────────────────
# STEP 4: The ReAct Loop — this is the core!
# ─────────────────────────────────────────────

def run_agent(user_question: str):
    """
    Run the full ReAct loop:
      1. Send the question to Claude (with tools available)
      2. If Claude calls a tool → run it → feed result back → repeat
      3. If Claude gives a text answer → we're done
    """
    
    # Create the Anthropic client (reads ANTHROPIC_API_KEY from environment)
    client = anthropic.Anthropic()
    
    # The system prompt tells Claude HOW to behave as an agent.
    # This is your "personality + instructions" for the AI.
    system_prompt = """You are a research agent. Your job is to thoroughly research 
any topic the user asks about.

RULES:
- ALWAYS search at least 2 different angles before summarizing
- Use the search tool to find information
- Use the summarize tool to condense your findings
- Think step by step about what you still need to find out
- After gathering enough info, give a clear final answer

Be thorough. Don't rush to a conclusion after just one search."""

    # Start the conversation with the user's question
    messages = [
        {"role": "user", "content": user_question}
    ]
    
    loop_count = 0
    max_loops = 10  # Safety limit so it doesn't run forever
    
    print(f"\n{'='*60}")
    print(f"🤖 AGENT STARTING — Question: {user_question}")
    print(f"{'='*60}\n")
    
    # ── THE LOOP ──
    while loop_count < max_loops:
        loop_count += 1
        print(f"── Loop {loop_count} ──")
        
        # 1. REASON — Ask Claude what to do next
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            tools=tools,
            messages=messages
        )
        
        # 2. Check: did Claude call a tool, or give a final answer?
        
        # Claude's response can have multiple "blocks":
        #   - "text" blocks = Claude thinking or giving final answer
        #   - "tool_use" blocks = Claude wants to call a tool
        
        # Check the stop_reason to know what happened:
        #   "tool_use"  = Claude wants to use a tool (keep looping)
        #   "end_turn"  = Claude is done (exit the loop)
        
        if response.stop_reason == "tool_use":
            # Claude wants to call one or more tools
            
            # First, print any thinking Claude did
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"  💭 Claude thinks: {block.text}")
            
            # Find all tool calls in the response
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  🔧 Claude calls: {block.name}({json.dumps(block.input)})")
                    
                    # 3. ACT — Run the tool
                    result = run_tool(block.name, block.input)
                    
                    # Save the result to send back to Claude
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,    # Must match the tool_use block's ID
                        "content": result
                    })
            
            # 4. OBSERVE — Add Claude's response + tool results to the conversation
            # so Claude can see what happened
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            
            # Loop back to REASON (top of while loop)
            
        else:
            # Claude gave a final answer (stop_reason == "end_turn")
            final_answer = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_answer += block.text
            
            print(f"\n{'='*60}")
            print(f"✅ AGENT FINISHED after {loop_count} loops")
            print(f"{'='*60}")
            print(f"\n{final_answer}")
            return final_answer
    
    print("⚠️  Hit maximum loop limit — stopping.")
    return "Agent stopped: too many loops."


# ─────────────────────────────────────────────
# STEP 5: Run it!
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Try changing this question to anything you want!
    run_agent("What are AI agents and why are companies excited about them in 2025?")
