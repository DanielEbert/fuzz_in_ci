from __future__ import annotations

from typing import Sequence
import os
import subprocess

from fuzzer import used_files


def build_executables() -> list[str]:
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../test_target')

    build_dir = os.path.join(target_path, 'build')
    if os.path.exists(build_dir):
        subprocess.check_call(['rm', '-r', build_dir])
    
    os.mkdir(build_dir)

    subprocess.check_call(['cmake', '..'], cwd=build_dir)
    subprocess.check_call(['cmake', '--build', '.'], cwd=build_dir)

    return [os.path.normpath(os.path.join(build_dir, f)) for f in ['exe_a', 'exe_b']]


def main(argv: Sequence[str] | None = None) -> int:
    print('Running fuzzer')

    executable_paths = build_executables()

    for executable_path in executable_paths:
        used_elf_files = used_files.get_used_files(executable_path)
        print(f'{used_elf_files=}')
    
    # i know that path starting from /*/HERE is always the same, no matter where its build. /*/ is the subsys name

    print(executable_paths)

    return 0

if __name__ == '__main__':
    raise SystemExit(main())