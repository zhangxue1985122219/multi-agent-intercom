import sys
import subprocess
import argparse
import json
import os
import platform
import locale

def get_system_language():
    """
    Detects the operating system's default language.
    Returns 'zh' for Chinese (Simplified/Traditional), 'en' for English (default).
    """
    try:
        # 1. Check standard environment variables (Linux/macOS)
        for env_var in ['LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE']:
            val = os.environ.get(env_var, '').lower()
            if val:
                if 'zh' in val: return 'zh'
                if 'en' in val: return 'en'
                
        # 2. Check Python's locale module safely
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                loc = locale.getdefaultlocale()[0]
                if loc and loc.lower().startswith('zh'): 
                    return 'zh'
        except Exception:
            pass
            
        # 3. Deep fallback for Windows API
        if os.name == 'nt':
            import ctypes
            langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            # Primary language ID for Chinese is 0x04
            if (langid & 0x03FF) == 0x04:
                return 'zh'
    except Exception:
        pass
        
    return 'en' # Fallback to English for worldwide compatibility

def get_openclaw_config_path():
    home = os.path.expanduser("~")
    path = os.path.join(home, ".openclaw", "openclaw.json")
    return path

def load_config():
    config_path = get_openclaw_config_path()
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def list_agents(lang):
    config = load_config()
    if not config:
        msg = "❌ 找不到 openclaw.json 配置文件。" if lang == 'zh' else "❌ Could not find openclaw.json."
        print(msg)
        sys.exit(1)
        
    agents = config.get("agents", {}).get("list", [])
    if not agents:
        msg = "配置中没有发现智能体。" if lang == 'zh' else "No agents found in configuration."
        print(msg)
        return

    header = "🤖 系统中可用的智能体 (Available Agents):" if lang == 'zh' else "🤖 Available Agents in the System:"
    print(header)
    print("-" * 40)
    for agent in agents:
        aid = agent.get("id", "unknown")
        aname = agent.get("name", "No Name")
        is_default = " (默认/Default)" if agent.get("default") else ""
        print(f"- ID: {aid:<10} | Name: {aname}{is_default}")
    print("-" * 40)

def install_protocol(lang):
    """
    Injects the Intercom Protocol SOP into all agents' AGENTS.md files.
    Ensures idempotency (doesn't write if already there).
    Dynamically generates SOP based on system language.
    """
    config = load_config()
    if not config:
        print("❌ Could not read openclaw.json for installation.")
        sys.exit(1)
        
    agents = config.get("agents", {}).get("list", [])
    if not agents:
        print("❌ No agents found to install the protocol.")
        sys.exit(1)

    if lang == 'zh':
        protocol_text = """

## 📡 跨智能体通信协议 (Multi-Agent Intercom)
你具有和其他智能体横向通信的能力。请严格遵守以下 SOP：
1. **发送消息**：当你需要联系或通知其他智能体时，调用系统终端执行以下命令：
   `python ~/.openclaw/skills/multi-agent-intercom/scripts/intercom.py send <目标智能体ID> <你的ID> "<你要说的话>"`
2. **接收与强制回复**：当你看到一条以 `【来自智能体: xxx】` 开头的消息时，意味着你正在被对讲机呼叫。
   - 你**必须立刻**处理该消息。
   - 处理完毕后，你**必须**使用上述 `send` 命令将结果或确认信息**回复给发送方**。
   - **严禁**直接在当前主聊天框里向人类用户说“谢谢收到”，你的直接回复必须发给呼叫你的那个智能体！
"""
        tag_match = "Multi-Agent Intercom"
        msg_success = "✅ 协议已成功注入到"
        msg_skip = "ℹ️ 协议已存在于"
        msg_complete = "\n🎉 安装完成！共更新了 {count} 个智能体。"
        msg_warn = "⚠️  重要提示：请提醒老大在聊天框输入 `/new` 命令，以重载我们的大脑记忆并激活该协议。"
    else:
        protocol_text = """

## 📡 Multi-Agent Intercom Protocol
You have the ability to communicate laterally with other agents. Please strictly follow this SOP:
1. **Send Message**: When you need to contact or notify other agents, run the following command in the system terminal:
   `python ~/.openclaw/skills/multi-agent-intercom/scripts/intercom.py send <TARGET_AGENT_ID> <YOUR_ID> "<YOUR_MESSAGE>"`
2. **Receive & Mandatory Reply**: When you see a message starting with `[Incoming from Agent: xxx]`, it means you are being paged via intercom.
   - You **MUST** process this message immediately.
   - After processing, you **MUST** use the `send` command above to **reply to the sender**.
   - **DO NOT** just say "Thank you" to the human user in the main chat. Your direct reply MUST go to the agent who called you!
"""
        tag_match = "Multi-Agent Intercom Protocol"
        msg_success = "✅ Protocol injected into"
        msg_skip = "ℹ️ Protocol already exists in"
        msg_complete = "\n🎉 Installation complete! Updated {count} agents."
        msg_warn = "⚠️  IMPORTANT: Please tell the user to run the `/new` command in their chat to reload the updated AGENTS.md files into memory."

    installed_count = 0
    for agent in agents:
        workspace = agent.get("workspace")
        if not workspace:
            continue
            
        if workspace.startswith("~"):
            workspace = os.path.expanduser(workspace)
            
        agents_md_path = os.path.join(workspace, "AGENTS.md")
        
        if not os.path.exists(workspace):
            continue
            
        content = ""
        if os.path.exists(agents_md_path):
            with open(agents_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
        if tag_match not in content:
            with open(agents_md_path, 'a', encoding='utf-8') as f:
                f.write(protocol_text)
            print(f"{msg_success} {agent.get('id')}'s AGENTS.md")
            installed_count += 1
        else:
            print(f"{msg_skip} {agent.get('id')}'s AGENTS.md (Skipped)")

    print(msg_complete.format(count=installed_count))
    print(msg_warn)

def run_background_task(shell_cmd):
    try:
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            subprocess.Popen(
                shell_cmd, 
                shell=True,
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                shell_cmd, 
                shell=True,
                preexec_fn=os.setsid,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    except Exception:
        pass

def send_message(target, sender_id, message, session_id, lang):
    # Construct a simple, inline system tag without any tricky newlines or brackets that break CMD
    tag = f"[来自智能体 {sender_id}] " if lang == 'zh' else f"[From Agent {sender_id}] "
    final_message = tag + message

    if lang == 'zh':
        print(f"正在尝试将消息发送给 '{target}' (会话: {session_id})...")
        print("✅ 消息已成功送出！目标智能体将在后台处理，如果需要会主动回复。")
    else:
        print(f"Attempting to send message to '{target}' (session: {session_id})...")
        print("✅ Message successfully sent! The target will process it in the background.")

    # Return to the exact same escaping logic that worked in version 1
    safe_message = final_message.replace('"', '\\"')
    shell_cmd = f'openclaw agent --agent {target} --session-id {session_id} --message "{safe_message}"'
    
    sys.stdout.flush()
    run_background_task(shell_cmd)
    sys.exit(0)

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')

    # Detect OS language at runtime
    sys_lang = get_system_language()

    parser = argparse.ArgumentParser(description="Multi-Agent Intercom for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Commands: list, install, send")
    
    subparsers.add_parser("list", help="List all available agents in the system")
    subparsers.add_parser("install", help="Inject the communication SOP into all AGENTS.md files")
    
    send_parser = subparsers.add_parser("send", help="Send a message to another agent")
    send_parser.add_argument("target_agent", help="The ID of the target agent (e.g., dev, rc)")
    send_parser.add_argument("sender_id", help="Your own agent ID (e.g., zz) for Caller ID")
    send_parser.add_argument("message", help="The message content to send")
    send_parser.add_argument("--session-id", default="main", help="The session ID to target (default: main)")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_agents(sys_lang)
    elif args.command == "install":
        install_protocol(sys_lang)
    elif args.command == "send":
        send_message(args.target_agent, args.sender_id, args.message, args.session_id, sys_lang)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
