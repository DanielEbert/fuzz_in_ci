from __future__ import annotations

import sys
import tempfile
import subprocess
import os

def run_gdb(elf_path, command, timeout_sec: float = 5) -> str:
    with tempfile.TemporaryDirectory() as tmp_dir:
        gdb_logpath = os.path.join(tmp_dir, 'gdb_log.txt')
        subprocess.check_call(
            [
                'gdb',
                '--ex', 'set pagination off',
                '--ex', 'set confirm off',
                '--ex', f'set logging file {gdb_logpath}',
                '--ex', 'set logging enabled on',
                '--ex', command,
                '--ex', 'set logging enabled off',
                '--ex', 'q',
                elf_path
            ],
            timeout=timeout_sec,
            stdout=subprocess.DEVNULL
        )

        with open(gdb_logpath) as f:
            gdb_output = f.read()
        
        return gdb_output


def get_used_files(elf_path: str) -> list(str):
    used_files = []

    gdb_output = run_gdb(elf_path, 'info sources')

    for line in gdb_output.splitlines():
        if not any([line.endswith(ending) for ending in ['.hpp', '.h', '.cpp', '.c', '.cc', '.hh']]):
            continue
        used_files.extend([filename.strip() for filename in line.split(',')])

    return used_files

def main() -> int:
    used_files = get_used_files(sys.argv[1])

    print(used_files)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())