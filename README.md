# CK-CLI Tools

Several tools that can be added to your `PATH` to make your life easier.

## `prettypath`

Prints the `$PATH` variable in a human-readable way. It also lets you search for or ignore patterns.

**Example:**
```
ck@laptop:~$ prettypath --help
usage: prettypath [-h] [-s SEARCH] [-i IGNORE]

Print the `PATH` variable in a human-readable way.

options:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        Only show path directories matching this pattern
  -i IGNORE, --ignore IGNORE
                        Ignore path directories matching this pattern
ck@laptop:~$ prettypath -i /mnt/c/
/home/ck/.local/bin
/home/ck/bin
/home/ck/ckvenv/bin
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
/sbin
/bin
/usr/games
/usr/local/games
/snap/bin
ck@Laptop-CK:~$
```

## `schedcom`

Schedule a task and/or get notified when it finishes.

```
ck@laptop:~$ schedcom --help
usage: schedcom.py [-h] [-n] (-a STARTTIME | -i DELAY) command

Schedule a task and/or get notified when it finishes

positional arguments:
  command               The command to be scheduled. Surround the command with quotation marks if it contains spaces.

optional arguments:
  -h, --help            show this help message and exit
  -n, --notify          Send a notification message via Telegram after the command is finished executing
  -a STARTTIME, --at STARTTIME
                        time to start at. Format: YYYY-MM-DDTHH:MM:SS
  -i DELAY, --in DELAY  run the command after a delay. Example: "1d3h36m34s"
ck@laptop:~$ schedcom --in 3s ls
Executing ls in 3 s.
executing...
bin  documents  downloads
"ls" executed successfully!
```
