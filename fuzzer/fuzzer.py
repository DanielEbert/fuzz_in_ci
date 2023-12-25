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

def get_changed_files() -> list[str]:
    base_commit = subprocess.check_output(['git', 'merge-base', 'HEAD', 'main'], text=True).strip()
    paths = subprocess.check_output(['git', 'diff', '--name-only', f'{base_commit}..'], text=True).splitlines()
    return [os.path.basename(path) for path in paths]


def executable_has_changed(executable_path: str, diff_changed_files: list[str]) -> bool:
    exe_changed_paths = used_files.get_used_files(executable_path)
    exe_changed_files = [os.path.basename(path) for path in exe_changed_paths]
    return set(exe_changed_files) & set(diff_changed_files)

def main(argv: Sequence[str] | None = None) -> int:
    print('Running fuzzer')

    executable_paths = build_executables()
    
    # i know that path starting from /*/HERE is always the same, no matter where its build. /*/ is the subsys name

    diff_changed_files = get_changed_files()

    print(get_changed_files())

    changed_exes = [exe for exe in executable_paths if executable_has_changed(exe, diff_changed_files)]

    print(f'{changed_exes=}')

    return 0

if __name__ == '__main__':
    raise SystemExit(main())