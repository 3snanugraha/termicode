# Session & Context Management Guide

## Overview

Termicode supports conversation context management to handle:
- **Session Persistence**: Save and load conversations
- **Token Limits**: Automatically truncate context to prevent API overflow
- **Context Monitoring**: Track token usage in real-time

---

## How Context Works

### Memory-Only Mode (Default)

By default, termicode keeps conversation in **memory only**:

```python
assistant = CodingAssistant()
```

**Behavior:**
- ✅ Fast and simple
- ✅ No file I/O overhead
- ❌ Context lost when you exit
- ❌ Cannot resume previous conversations

**When to use:** Quick sessions, testing, single-task workflows

---

### Session Persistence Mode

Enable session persistence to save conversations locally:

```python
assistant = CodingAssistant(
    enable_session=True,
    session_name="my_project_session"
)
```

**Behavior:**
- ✅ Conversation saved to `.termicode_sessions/` folder
- ✅ Resume conversations later
- ✅ Automatic save after each response
- ⚠️ Slightly slower (file I/O)

**When to use:** Long projects, debugging sessions, multi-day work

---

## Session Files

Sessions are stored as JSON files in `.termicode_sessions/`:

```
.termicode_sessions/
├── session_20250101_143022.json
├── project_alpha.json
└── debugging_session.json
```

**File format:**
```json
{
  "created_at": "2025-10-01T14:30:22",
  "message_count": 12,
  "history": [
    {
      "role": "user",
      "content": "Show me all Python files"
    },
    {
      "role": "assistant",
      "content": "I'll search for Python files..."
    }
  ]
}
```

---

## Context Management (Token Limits)

### The Problem

AI models have **token limits**. For example:
- DeepSeek-V3: ~32K tokens (~24K words)
- If you exceed this, API calls **fail**

### The Solution

Termicode automatically manages context with `ContextManager`:

```python
context_manager = ContextManager(
    max_messages=20,        # Keep last 20 messages
    max_tokens_estimate=8000  # Rough token limit
)
```

**Strategy:**
1. **Estimate tokens** (rough: 4 chars ≈ 1 token)
2. **Truncate old messages** when limit reached
3. **Keep recent messages** (most relevant)
4. **Warn user** when context is full

---

## Using Context Commands

### Check Context Usage

Use the `context` command in termicode:

```bash
You ▶ context

Context Information:
  Messages: 8 (4 user, 4 assistant)
  Estimated tokens: 2450 / 8000
  Usage: 30.6%
```

### Clear Context

Use `clear` command to reset:

```bash
You ▶ clear

✓ Conversation history cleared.
```

**Note:** If sessions are enabled, this saves an empty history.

---

## API Reference

### CodingAssistant Class

```python
from src.assistant import CodingAssistant

assistant = CodingAssistant(
    model="deepseek-ai/DeepSeek-V3.2-Exp",  # AI model
    interactive=True,                        # Interactive UI
    enable_session=False,                    # Enable persistence
    session_name=None                        # Session name (auto if None)
)
```

### Get Context Info

```python
info = assistant.get_context_info()

print(info)
# {
#     'total_messages': 8,
#     'user_messages': 4,
#     'assistant_messages': 4,
#     'estimated_tokens': 2450,
#     'tokens_remaining': 5550,
#     'usage_percentage': 30.6
# }
```

---

## SessionManager API

### Creating Sessions

```python
from src.utils.session_manager import SessionManager

manager = SessionManager()

# Auto-generate session name
session_file = manager.create_session()
# → .termicode_sessions/session_20250101_143022.json

# Named session
session_file = manager.create_session("my_project")
# → .termicode_sessions/my_project.json
```

### Loading Sessions

```python
history = manager.load_session("my_project")
# Returns: List[Dict[str, str]]
```

### Listing Sessions

```python
sessions = manager.list_sessions()

for session in sessions:
    print(f"{session['name']}: {session['message_count']} messages")
# my_project: 12 messages
# debugging: 8 messages
```

### Deleting Sessions

```python
manager.delete_session("old_session")
```

---

## ContextManager API

### Truncation Strategies

#### 1. Token-Based Truncation (Default)

Keep messages that fit within token limit:

```python
truncated = context_manager.truncate_history(
    history=conversation_history,
    system_prompt="You are a coding assistant"
)
```

#### 2. Sliding Window

Keep only last N message pairs:

```python
recent = context_manager.sliding_window(
    history=conversation_history,
    window_size=10  # Last 10 pairs (20 messages)
)
```

#### 3. Compression

Keep first and last messages, summarize middle:

```python
compressed = context_manager.compress_history(
    history=conversation_history,
    keep_recent=4  # Keep last 4 messages
)
```

---

## Configuration

### Environment Variables

Add to `.env`:

```bash
# Enable session by default (planned feature)
SESSION_ENABLED=true

# Default session name
SESSION_NAME=default

# Context limits
MAX_MESSAGES=20
MAX_TOKENS=8000
```

### Customize Limits

```python
assistant = CodingAssistant(enable_session=True)

# Change context limits
assistant.context_manager.max_messages = 30
assistant.context_manager.max_tokens_estimate = 12000
```

---

## Best Practices

### 1. Monitor Context Usage

Check context periodically in long sessions:

```bash
You ▶ context
```

If usage > 80%, consider clearing or saving important info.

### 2. Use Sessions for Projects

Enable sessions when working on projects:

```python
# In main.py
assistant = CodingAssistant(
    enable_session=True,
    session_name=f"project_{project_name}"
)
```

### 3. Clean Up Old Sessions

Delete unused sessions:

```python
manager = SessionManager()
manager.delete_session("old_debugging_2024")
```

### 4. Adjust Token Limits

For longer conversations:

```python
assistant.context_manager.max_tokens_estimate = 16000
```

For shorter (faster) conversations:

```python
assistant.context_manager.max_tokens_estimate = 4000
```

---

## Troubleshooting

### Issue: "Context full" warning

**Cause:** Too many messages in conversation

**Solutions:**
1. Use `clear` command to reset
2. Increase `max_tokens_estimate`
3. Enable compression strategy

### Issue: Session file corrupted

**Cause:** Interrupted write, JSON parse error

**Solution:** Delete corrupted file:
```bash
rm .termicode_sessions/corrupted_session.json
```

### Issue: Slow performance with sessions

**Cause:** File I/O overhead

**Solutions:**
1. Disable sessions for quick tasks
2. Use SSD storage
3. Reduce save frequency (code modification needed)

---

## Future Enhancements

- [ ] CLI commands: `/save`, `/load`, `/sessions`
- [ ] Automatic session naming based on working directory
- [ ] Session export/import (share with team)
- [ ] Context summarization with AI
- [ ] Vector database for long-term memory
- [ ] Multi-session management UI

---

## Example Usage

### Scenario 1: Quick Task (No Session)

```bash
$ termicode
You ▶ Read main.py
You ▶ Fix the bug in line 42
You ▶ exit
```

Context is lost after exit. ✅ Fast, simple.

### Scenario 2: Project Work (With Session)

```python
# Modified main.py to enable sessions
assistant = CodingAssistant(
    enable_session=True,
    session_name="refactor_project"
)
```

```bash
$ termicode
You ▶ Show me the project structure
You ▶ Let's refactor the authentication module
You ▶ exit

# Later...
$ termicode
You ▶ Continue refactoring
# AI remembers previous conversation! ✅
```

### Scenario 3: Context Monitoring

```bash
You ▶ context
Context Information:
  Messages: 24 (12 user, 12 assistant)
  Estimated tokens: 7200 / 8000
  Usage: 90.0%
  ⚠ Warning: Context is getting full. Consider using 'clear' command.

You ▶ clear
✓ Conversation history cleared.

You ▶ context
Context Information:
  Messages: 0 (0 user, 0 assistant)
  Estimated tokens: 0 / 8000
  Usage: 0.0%
```

---

## Summary

| Feature | Memory-Only | Session-Enabled |
|---------|-------------|-----------------|
| **Speed** | Fast | Slightly slower |
| **Persistence** | ❌ Lost on exit | ✅ Saved to disk |
| **Resume** | ❌ No | ✅ Yes |
| **Use Case** | Quick tasks | Project work |

**Default:** Memory-only (fast, simple)

**Recommended:** Enable sessions for serious work

**Always:** Monitor context with `context` command!
