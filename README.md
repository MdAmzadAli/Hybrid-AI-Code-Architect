# Hybrid-AI Code Architect

A Python-based Model Context Protocol (MCP) server that bridges multiple AI SDKs to:

- Generate optimized Python functions using Google Gemini
- Review generated code for security and performance issues using Anthropic Claude
- Automatically fall back to Gemini if Claude is unavailable
- Perform a one-step self-correction loop when issues are detected

---

## 🚀 Objective

This project demonstrates:

- Proper MCP tool implementation
- Multi-model orchestration
- Async programming in Python
- Strong prompt engineering
- Fault-tolerant AI architecture
- Clean and production-ready code structure

---

## 🏗 Architecture Overview

```
User Prompt
     ↓
Gemini → Generate Python Code
     ↓
Claude → Security & Performance Review
     ↓
If Claude fails → Gemini Fallback Reviewer
     ↓
If Issues Found → Self-Correction Loop (One Retry)
     ↓
Return Structured JSON Response
```

---

## 📁 Project Structure

```
hybrid-ai-code-architect/
│
├── server.py
│
├── services/
│   ├── gemini_service.py
│   └── claude_service.py
│
├── tests/
│   └── client_test.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## 🛠 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MdAmzadAli/Hybrid-AI-Code-Architect.git
cd Hybrid-AI-Code-Architect
```

### 2️⃣ Create Virtual Environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_claude_api_key   # Optional
```

> If the Claude API key is missing, the system automatically falls back to Gemini for review.

---

## ▶ Running the MCP Server

Start the server:

```bash
python server.py
```

> The server runs in stdio MCP mode and will remain silent while waiting for tool calls.  
> Do not type anything in that terminal.

---

## 🧪 Testing the Server

Open a second terminal and run:

```bash
python tests/client_test.py
```

This will:

- Connect to the MCP server
- Call the `generate_and_review` tool
- Print structured output

---

## 🧠 Tool: `generate_and_review`

**Input**
```json
{
  "prompt": "Write a function to calculate factorial iteratively."
}
```

**Output**
```json
{
  "generated_code": "def factorial(n: int) -> int: ...",
  "security_review": "LGTM",
  "reviewer_used": "claude"
}
```

---

## 🔁 Self-Correction Loop 

If the reviewer identifies issues:

1. The review feedback is sent back to Gemini
2. Gemini refactors the code once
3. The refactored code is reviewed again
4. The final result is returned

> Only one correction cycle is performed to prevent infinite loops.

---

## 🛡 Fault Tolerance

The system handles:

- Missing Claude API key
- Claude API failures
- Rate limits
- Empty model responses
- Invalid tool calls

### Fallback Strategy

| Scenario | Behavior |
|---|---|
| Claude unavailable | Gemini reviewer used |
| Claude API error | Gemini reviewer used |
| Review finds issues | Self-correction triggered |
| Critical failure | Structured error response returned |

---


## ⚙ Technologies Used

- Python 3.10+
- MCP Python SDK
- Google GenAI SDK
- Anthropic SDK
- asyncio
- python-dotenv
- Pydantic

---

## ⏱ Time Tracking

| | |
|---|---|
| Start Date | 28 February 2026 – 14:00 |
| Completion Date | 28 February 2026 – 19:00 |
| Total Time Taken | 5 hours |