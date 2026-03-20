# Multi-Agent Intercom

🗣️ **A powerful peer-to-peer communication skill for OpenClaw.**

This skill enables independent OpenClaw agents (e.g., `zz`, `dev`, `rc`) to securely send messages and wake up each other across isolated workspaces. It acts as an "intercom system" for your Multi-Agent setup.

## 🌟 Why is this needed?
By design, OpenClaw agents run in isolated databases and sandboxes. The built-in `sessions_send` tool can only send messages within an agent's own subagent hierarchy. If Agent A tries to use `sessions_send` to message Agent B, it will result in a "Session not found" error. 

**Multi-Agent Intercom** solves this by leveraging the native `openclaw agent` CLI mechanism to safely bridge these isolated environments, allowing agents to act as equal peers in a decentralized company.

## ✨ Features
- **Auto-Discovery**: Agents can automatically list all other agents configured on the current Gateway.
- **Cross-Boundary Messaging**: Send instructions or notifications to any agent on the same system.
- **Internationalization (i18n)**: Automatically detects the OS language and injects SOPs/Caller IDs in either English or Chinese.
- **Absolute Stealth (Cross-Platform)**: Executes asynchronously in the background. Zero terminal popups on Windows, fully detached on macOS/Linux.
- **Immediate Wake-up**: Bypasses sleep states and forces the target agent to process the message immediately.
- **Persistent Context**: Targets the `main` session by default, ensuring long-term context is preserved.

## 📦 Installation & Setup
If you downloaded this from ClawHub or GitHub:
1. Extract the folder into your `~/.openclaw/skills/` directory.
2. Ensure the OpenClaw CLI (`openclaw`) is accessible in your system's PATH.

**One-Time Initialization:**
Ask any of your agents to install the intercom protocol using natural language:
> *"请安装 multi-agent-intercom 技能"* 
> *(Or: "Please run the installation script for the multi-agent-intercom skill.")*

The agent will autonomously read the `SKILL.md` and run `python scripts/intercom.py install`. This safely injects the communication SOP into the `AGENTS.md` of every agent on your system. **After installation, type `/new` in your chat** to reload their brains with the new protocol.

## 🚀 How Agents Use It
Agents can use this skill autonomously when they determine they need to contact another agent. The scripts are entirely silent and cross-platform (no popup terminal windows on Windows or Mac).

**To list available agents:**
```bash
python scripts/intercom.py list
```

**To send a message:**
The syntax requires the sender to identify themselves so the receiver gets a proper "Caller ID".
```bash
python scripts/intercom.py send <TARGET_ID> <SENDER_ID> "Your message here"
```

**Example (Agent 'zz' messaging 'dev'):**
```bash
python scripts/intercom.py send dev zz "Hi dev, the user wants us to update our avatars. Please acknowledge."
```

When 'dev' receives this, the system automatically formats it with a clean, system-compatible tag:
`[来自智能体 dev] Your message here`
Thanks to the injected `AGENTS.md` SOP, 'dev' instantly knows how to reply using the exact same tool.

## 🛡️ Requirements
- OpenClaw >= 2026.x
- Python 3.x

---
*Created for the OpenClaw / ClawDBot community.*
