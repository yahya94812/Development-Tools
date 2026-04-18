# How Colab Works
## 1. Linux VM (aka runtime)
- When you open a Colab notebook, Google spins up a **Linux VM** (Virtual Machine with CPU/GPU, RAM, filesystem /content/, all running processes) for you. Everything — terminal, notebook, files — lives inside this one VM.
- Restart runtime means every thing except the notebook code is gone!.

## 2. Session
Your **connection** between your browser and the runtime VM.

- If you close the tab and reopen → new session, same runtime (if it didn't timeout)
- If runtime times out (idle ~90 min) → session + runtime both die
- One runtime = one session at a time

> Think of session as the **live wire** between you and the VM.

- in most of the cases session means the runtime (VM) it self

## 3. Kernel
The **Python process** that actually executes your notebook cells.

- It's a running `ipykernel` process inside the VM
- Holds all your variables, imports, state in memory
- "Restart Kernel" = kill just this Python process, restart fresh
- The filesystem is **not** affected by kernel restart

> Kernel is just the **Python interpreter** running your cells.

## 4. How Thet Relate
Google Cloud
└── VM (Runtime)
    ├── Filesystem (/content/)
    ├── Kernel (Python process → runs notebook cells)
    ├── Terminal (separate shell process)
    └── Session (your browser ↔ VM connection)

## 5. Are Terminal and Notebook Connected?

**Yes, partially — but not fully.**

|Thing|Terminal (`!cmd` or Tools→Terminal)|Notebook Kernel|
|---|---|---|
|Filesystem|✅ Same (`/content/`)|✅ Same|
|Environment variables|✅ Shared (if set before kernel starts)|⚠️ Not always synced|
|Python interpreter|❌ Different process|❌ Different process|
|`conda activate` effect|✅ Works in terminal|❌ Does NOT affect notebook|

So if you `conda activate myenv` in the terminal, **the notebook kernel won't switch** — because the kernel is a separate process already running its own Python.

## 6. Disadvantage of colab
1. the runtime is for short duration of time it get's disconnected too often as compare to kaggle where it can live upto (30 hr)
2. you can't save the runtime snapshot to load it later as in kaggle save and version option

## 7.File Structure
```
/# ls
bin      dev     lib     media  python-apt         sbin  tools
boot     etc     lib32   mnt    python-apt.tar.xz  srv   usr
content  home    lib64   opt    root               sys   var
datalab  kaggle  libx32  proc   run                tmp
```
- the default working directory is ```/content/```
- the ~/ directory is /root (not ~/home) because we don't have any user to this machine and we are directly working as a root user

## FAQs
what is the difference between command running in notebook with !, and command running in the terminal : in notebook the bash it started as a sub process it execute commands specified and destroyed
explain how ipykernel works under the hood : it is a separate process use the IPython under the hood 
while downloading the lib with pip does it able to change the path env var ; not directly but it can place files in /bin 
