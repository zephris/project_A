"""Run one deck with KiCad's ngspice DLL in an isolated worker process."""
import argparse
import ctypes as ct
import os
from pathlib import Path
import sys
import shutil
import tempfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dll', required=True)
    parser.add_argument('--version', action='store_true')
    parser.add_argument('--pspice', action='store_true')
    parser.add_argument('deck', nargs='?')
    args = parser.parse_args()
    path = Path(args.dll).resolve()
    dll_directory = os.add_dll_directory(str(path.parent)) if os.name == 'nt' else None
    library = ct.CDLL(str(path))
    messages = []
    exits = []
    char_type = ct.CFUNCTYPE(ct.c_int, ct.c_char_p, ct.c_int, ct.c_void_p)
    exit_type = ct.CFUNCTYPE(ct.c_int, ct.c_int, ct.c_bool, ct.c_bool, ct.c_int, ct.c_void_p)

    @char_type
    def send_char(message, ident, user):
        text = message.decode('utf-8', errors='replace')
        # ngspice prefixes callbacks with stdout/stderr; batch parser expects raw lines.
        text = text.removeprefix('stdout ').removeprefix('stderr ')
        messages.append(text)
        print(text, flush=True)
        return 0

    @exit_type
    def controlled_exit(status, immediate, quit_exit, ident, user):
        exits.append(status)
        return 0

    library.ngSpice_Init.argtypes = [char_type, ct.c_void_p, exit_type,
                                     ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p]
    library.ngSpice_Init.restype = ct.c_int
    library.ngSpice_Command.argtypes = [ct.c_char_p]
    library.ngSpice_Command.restype = ct.c_int
    library.ngSpice_Init(send_char, None, controlled_exit, None, None, None, None)
    library.ngSpice_Command(b'version')
    if args.version:
        return 0
    if not args.deck:
        parser.error('deck required')
    # The runner sets cwd to the case folder, making circuit.inc portable.
    # Use the local filename: shared ngspice treats quoted source names literally.
    os.chdir(Path(args.deck).resolve().parent)
    if args.pspice:
        # DLL startup lacks KiCad's spinit. Windows codemodel rejects spaced paths.
        cm_root = path.parent.parent / 'lib' / 'ngspice'
        code_dir = Path(tempfile.mkdtemp(prefix='phbox_ngspice_'))
        if ' ' in str(code_dir):
            raise RuntimeError('XSPICE temporary directory must have no spaces')
        for name in ['analog', 'table', 'digital', 'spice2poly', 'tlines', 'xtradev', 'xtraevt']:
            target = code_dir / (name + '.cm')
            shutil.copy2(cm_root / target.name, target)
            if library.ngSpice_Command(('codemodel ' + target.as_posix()).encode()):
                raise RuntimeError('Cannot load ' + name)
        # Loaded .cm DLLs remain locked until this isolated process exits.
        library.ngSpice_Command(b'set ngbehavior=ps')
    source = library.ngSpice_Command(('source ' + Path(args.deck).name).encode())
    if source or exits:
        return 1
    result = library.ngSpice_Command(b'run')
    if result or exits:
        return 1
    # Keep the raw vectors for later waveform inspection; measurements are in stdout.
    library.ngSpice_Command(b'write waveform.raw all')
    return 0

if __name__ == '__main__':
    sys.exit(main())
