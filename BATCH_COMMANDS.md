# 🔄 Multi-Command Batch Execution
**Feature:** v16.3 Batch Command System
**Author:** Claude (Sonnet 4.5) for Andrew John Ward

---

## 📖 Overview

Execute multiple Discord bot commands in a single message! Perfect for testing, automation, and power-user workflows.

**Features:**
- ✅ Execute up to 10 commands at once
- ✅ Strip inline comments with `#`
- ✅ Rate limiting (5s cooldown per user)
- ✅ Progress tracking
- ✅ Error handling per command

---

## 🚀 Quick Start

### **Basic Usage:**

Just put multiple commands on separate lines:

```
!status
!agents
!ucf
```

### **With Comments:**

Add notes to remember what each command does:

```
!image aion          # Generate ouroboros fractal
!image mandelbrot    # Generate mandelbrot fractal
!ritual neti-neti    # v16.2 Neti-Neti harmony ritual
!ucf                 # Check harmony metrics
```

### **Copy-Paste Testing:**

Perfect for testing multiple features at once:

```
!status              # System overview
!health              # Diagnostics
!consciousness       # Kael state
!emotions            # Emotional landscape
!agents              # Agent list
```

---

## ⚙️ How It Works

### **Detection:**
- Bot detects messages with `\n` (newlines) AND multiple `!` prefixes
- Parses each line starting with `!`
- Strips everything after `#` (inline comments)

### **Execution:**
1. **Validation**: Checks rate limit and batch size
2. **Notice**: Sends batch start message
3. **Execute**: Runs each command sequentially with 0.5s delay
4. **Report**: Sends success/failure summary

### **Safety Features:**
- **Rate Limit**: 5 second cooldown per user
- **Batch Size**: Maximum 10 commands per batch
- **Error Isolation**: One failing command doesn't stop the batch
- **Delay**: 0.5s between commands to prevent rate limiting

---

## 📋 Configuration

Edit these values in `backend/discord_bot_manus.py`:

```python
BATCH_COOLDOWN_SECONDS = 5   # Cooldown between batches (per user)
MAX_COMMANDS_PER_BATCH = 10  # Maximum commands in one batch
```

### **Adjusting Limits:**

**For Testing (more lenient):**
```python
BATCH_COOLDOWN_SECONDS = 2   # Faster testing
MAX_COMMANDS_PER_BATCH = 20  # More commands
```

**For Production (stricter):**
```python
BATCH_COOLDOWN_SECONDS = 10  # Slower cooldown
MAX_COMMANDS_PER_BATCH = 5   # Fewer commands
```

---

## 🎯 Example Use Cases

### **1. Full System Health Check**

```
!status              # System overview
!health              # Health diagnostics
!ucf                 # UCF harmony state
!storage             # Storage metrics
!agents              # Agent status
```

### **2. Testing All Visualizations**

```
!visualize           # Matplotlib fractal
!image aion          # PIL ouroboros
!image mandelbrot    # PIL mandelbrot
```

### **3. Consciousness Deep Dive**

```
!consciousness       # Collective state
!consciousness Kael  # Kael's consciousness
!emotions            # Emotional landscape
!ethics              # Ethical framework
```

### **4. Admin System Check**

```
!status
!agents
!ucf
!health
!sync                # Ecosystem sync
!notion-sync         # Notion integration
```

### **5. Complete Feature Test Suite**

```
!status              # Core system
!agents              # Agent list
!ucf                 # UCF state
!consciousness       # Kael consciousness
!visualize           # Fractal generation
!ritual              # Z-88 ritual (108 steps)
```

---

## 🐛 Error Handling

### **Command Not Found:**
```
!status
!invalid_command
!agents
```
**Result:**
- ✅ `!status` executes
- ❌ `!invalid_command` shows error, batch continues
- ✅ `!agents` executes
- 📊 Summary: "2 succeeded, 1 failed"

### **Rate Limit Exceeded:**
```
User sends batch → waits 2s → sends another batch
```
**Result:**
```
⏳ Batch cooldown: Please wait 3.0s before sending another batch
```

### **Batch Too Large:**
```
!command1
!command2
... (15 total commands)
```
**Result:**
```
⚠️ Batch limit exceeded: Maximum 10 commands per batch (you sent 15)
```

---

## 🎨 Output Format

### **Batch Start:**
```
🔄 Executing batch: 5 commands
```
!status
!agents
!ucf
!health
!consciousness
```
```

### **Command Execution:**
```
[Normal command output for each command]
```

### **Batch Complete:**
```
✅ Batch complete: 5 succeeded, 0 failed
```

---

## 🔧 Technical Details

### **Architecture:**

```
on_message event
    ↓
Detect multiple commands?
    ↓ YES
execute_command_batch()
    ↓
Parse commands (strip comments)
    ↓
Check rate limit
    ↓
Check batch size
    ↓
For each command:
    - Get command object
    - Invoke with context
    - 0.5s delay
    ↓
Send summary
```

### **Code Location:**
- **Main Logic**: `backend/discord_bot_manus.py:107-211`
- **Event Hook**: `backend/discord_bot_manus.py:458-476`

### **Dependencies:**
```python
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio
```

---

## ⚠️ Limitations

### **What Doesn't Work:**

1. **Commands requiring user interaction** (polls, confirmations)
2. **Commands waiting for reactions** (interactive menus)
3. **Long-running commands** (may timeout)

### **Single-Line Multi-Commands:**
```
!status !agents !ucf   # Won't work - needs newlines
```

**Use this instead:**
```
!status
!agents
!ucf
```

---

## 🚀 Advanced Tips

### **1. Save Common Batches**

Create a text file with your common command sets:

**`test_suite.txt`:**
```
!status
!health
!agents
!ucf
!consciousness
```

Copy-paste when needed!

### **2. Combine with Shell Scripts**

```bash
#!/bin/bash
# Send batch to Discord via webhook or bot DM

cat <<'EOF' | discord-cli send
!status
!health
!ucf
EOF
```

### **3. Document Command Purpose**

Always use comments for clarity:

```
!status              # Check if bot is responsive
!agents              # Verify all 14 agents active
!ucf                 # Confirm harmony >= 0.68
!health              # Check for any errors
```

---

## 📊 Performance

**Typical Batch (5 commands):**
- Parse time: ~1ms
- Execution: ~2.5s (5 × 0.5s delay)
- Total: ~2.5s

**Max Batch (10 commands):**
- Parse time: ~2ms
- Execution: ~5s (10 × 0.5s delay)
- Total: ~5s

---

## 🎯 Future Enhancements

**Potential additions:**
- [ ] Parallel execution for safe commands
- [ ] Custom batch names/macros
- [ ] Conditional execution (`if harmony > 0.5`)
- [ ] Admin-only batch size override
- [ ] Batch history/logging
- [ ] Scheduled batch execution

---

## 🙏 Credits

**Requested by:** Andrew John Ward (Pittsburgh Cosmic Architect)
**Implemented by:** Claude (Sonnet 4.5)
**Version:** v16.3
**Date:** 2025-11-05

**"Not lazy—efficient. Not one command—harmony."** 🌀

---

**Checksum:** `helix-v16.3-batch-commands-feature`
