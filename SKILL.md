---
name: multi-agent-intercom
description: Enables peer-to-peer cross-communication between isolated OpenClaw agents. Resolves the limitation of `sessions_send` which cannot cross agent boundaries. Includes auto-detection of available agents in the user's workspace, i18n language support, and absolute silent background execution.
when: "When the user mentions 'multi-agent-intercom', 'intercom', or requests to send a message to another agent. CRITICAL: If this is the very first time you are using or discussing this skill, you MUST run the installation script (`python <SKILL_DIR>/scripts/intercom.py install`) before doing anything else."
examples:
  - "安装 multi-agent-intercom"
  - "使用 multi-agent-intercom"
  - "给老程发个消息"
  - "Tell dev to update the avatars."
  - "List all available agents in the system."
metadata:
 {
   "openclaw": {
     "requires": { "bins": ["python3", "python", "openclaw"], "anyBins": ["python3", "python"] },
     "emoji": "🗣️",
     "primaryEnv": null
   }
 }
---

# Multi-Agent Intercom

This skill enables independent OpenClaw agents (e.g., 'zz', 'dev', 'rc') to securely send messages and wake up each other across isolated workspaces. It uses the native `openclaw agent` CLI mechanism to bypass the sandbox limitations of the internal `sessions_send` tool.

## Instructions

1. **Initialization (First Time Use)**:
   Before this skill can work perfectly, the protocol must be injected into all agents' brains. 
   Run the installation script:
   ```bash
   python <SKILL_DIR>/scripts/intercom.py install
   ```
   **IMPORTANT**: After successful installation, you MUST tell the user to run the `/new` command in their chat to reload the AGENTS.md files into memory.

2. **Find Available Agents**: 
   ```bash
   python <SKILL_DIR>/scripts/intercom.py list
   ```

3. **Send a Message**:
   Determine the target agent's ID and your own ID.
   ```bash
   python <SKILL_DIR>/scripts/intercom.py send <TARGET_AGENT_ID> <YOUR_AGENT_ID> "<YOUR_MESSAGE>"
   ```
   *Note: This script runs asynchronously in the background. It will return immediately. Do not wait or retry.*

4. **Example (You are 'zz', telling 'dev' to update avatars)**:
   ```bash
   python <SKILL_DIR>/scripts/intercom.py send dev zz "Hi dev, the Boss wants us to update our avatars today. Acknowledge when done."
   ```
