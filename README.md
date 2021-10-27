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