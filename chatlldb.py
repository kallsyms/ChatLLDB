from urllib.request import Request, urlopen
import json
import pathlib
import lldb


CONFIG_FILE = pathlib.Path.home() / '.config' / 'chatlldb.conf'
# Ripped straight from ChatGDB, https://github.com/pgosar/ChatGDB
HEADERS = {
    "Content-Type": "application/json"
}
URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-3.5-turbo"
COMMAND_PROMPT = "Give me a SINGLE LLDB command with no explanation. Do NOT \
write any English above or below the command. Only give me the command as \
text. Here is my question: "
GDB_EQUIV_PROMPT = COMMAND_PROMPT + "what is the LLDB equivalent of the GDB command: "


def complete(query):
    req = Request(
            URL,
            headers=HEADERS,
            data=json.dumps({
                "model": MODEL,
                "messages": [{
                    "role": "user",
                    "content": query,
                }],
            }).encode('utf-8')
    )

    with urlopen(req, timeout=10) as response:
        resp = json.loads(response.read())
        return resp['choices'][0]['message']['content']


def chat(debugger, command, _result, _internal_dict):
    try:
        cmd = complete(COMMAND_PROMPT + command)
        print(f"-> {cmd}")
        debugger.HandleCommand(cmd)
    except Exception as e:
        print(f"Error getting completion: {e}")


def gdb(debugger, command, _result, _internal_dict):
    try:
        cmd = complete(GDB_EQUIV_PROMPT + command)
        print(f"-> {cmd}")
        debugger.HandleCommand(cmd)
    except Exception as e:
        print(f"Error getting completion: {e}")


def __lldb_init_module(debugger, _internal_dict):
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as config:
            HEADERS["Authorization"] = "Bearer " + config.read().strip()
        debugger.HandleCommand('command script add -f chatlldb.chat chat')
        debugger.HandleCommand('command script add -f chatlldb.gdb gdb')
        print("ChatLLDB loaded")
    else:
        print("ChatLLDB: No ChatGPT API key configured.")
        print(f"Put your key in {CONFIG_FILE}")
