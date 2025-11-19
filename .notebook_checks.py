import sys, os, traceback
from pathlib import Path
import re
import importlib

print('=== CHECK 1: Environment info ===')
print('cwd:', os.getcwd())
project_root = os.path.abspath(os.path.join(os.getcwd()))
# If running inside src, use cwd
if os.path.basename(project_root).lower() == 'src':
    src_dir = project_root
else:
    src_dir = os.path.join(project_root, 'src')
print('project_root:', project_root)
print('src_dir:', src_dir)
print('src_dir exists:', os.path.isdir(src_dir))
print('sys.executable:', sys.executable)
print('venv markers present:', os.path.isdir('.venv') or os.path.isdir(os.path.join(project_root, '.venv')))
print('\n')

print('=== CHECK 2: Safe viewer on src/mcp_server/server.py ===')
server_path = Path(src_dir) / 'mcp_server' / 'server.py'
print('server_path:', server_path.resolve() if server_path.exists() else server_path)
if not server_path.exists():
    print('server.py not found')
else:
    text = server_path.read_text(encoding='utf-8')
    imports = re.findall(r'^(import .+|from .+ import .+)$', text, flags=re.MULTILINE)
    print('\n-- imports (first 30) --')
    for line in imports[:30]:
        print(' ', line)
    classes = re.findall(r'^\s*class\s+([A-Za-z0-9_]+)\s*(?:\(|:)', text, flags=re.MULTILINE)
    functions = re.findall(r'^\s*def\s+([A-Za-z0-9_]+)\s*\(', text, flags=re.MULTILINE)
    print('\n-- classes --')
    print(classes)
    print('\n-- functions (first 50) --')
    print(functions[:50])
    print('\n-- preview (first 1000 chars) --')
    print(text[:1000])

print('\n')
print('=== CHECK 3: Smoke imports for project modules ===')
modules = ['mcp_server.server', 'mcp_client.client', 'core.document_processor', 'core.models']
added = False
try:
    # Temporarily ensure src_dir is on sys.path so importlib can find project packages
    if os.path.isdir(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        added = True
    for m in modules:
        try:
            mod = importlib.import_module(m)
            print(f'Imported {m} ->', getattr(mod, '__file__', 'built-in/namespace'))
        except Exception as e:
            print(f'Failed to import {m}: {e}')
            traceback.print_exc()
finally:
    if added:
        try:
            sys.path.remove(src_dir)
        except ValueError:
            pass

print('\nAll checks completed')

print('\n=== CHECK 4: Ollama reachability probe (localhost:11434) ===')
import socket
from urllib.parse import urljoin
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    try:
        sock.connect(('127.0.0.1', 11434))
        print('TCP connect to 127.0.0.1:11434 -> OK')
        # Optionally do a small HTTP GET if requests/httpx available
        try:
            import httpx
            try:
                r = httpx.get('http://127.0.0.1:11434/')
                print('HTTP GET / ->', r.status_code)
                print('Response snippet:', r.text[:200])
            except Exception as e:
                print('HTTP probe failed:', e)
        except Exception:
            print('httpx not available in venv; skipping HTTP probe')
    except Exception as e:
        print('TCP connect to 127.0.0.1:11434 -> FAILED:', e)
    finally:
        sock.close()
except Exception as e:
    print('Ollama probe encountered an unexpected error:', e)
