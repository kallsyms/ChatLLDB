# ChatLLDB

Use ChatGPT to make it easier to interact with lldb.

Basically just [ChatGDB](https://github.com/pgosar/ChatGDB) for lldb :)

## Installation

1. `git clone https://github.com/kallsyms/ChatLLDB`
1. Add to your `~/.lldbinit`: `command script import /path/to/ChatLLDB/chatlldb.py`
1. Grab your ChatGPT auth token and save it to `~/.config/chatlldb.conf`


## Usage

ChatLLDB adds 2 commands to lldb:

* `chat {query}`: Translate the human readable `query` into a lldb command, and run it.
* `gdb {command}`: Translate the GDB command `command` into a lldb command, and run it.


### Examples:

```
(lldb) chat breakpoint at function main
-> breakpoint set --name main
Breakpoint 1: where = t`main, address = ...
```

```
(lldb) gdb start
-> process launch
...
```
