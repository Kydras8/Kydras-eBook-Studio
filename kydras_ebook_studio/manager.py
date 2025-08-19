import os, sys, subprocess, socket, time
from pathlib import Path

APPDIR = Path(__file__).resolve().parents[1]
LOGDIR = Path.home()/".local"/"state"/"kydras-ebook-studio"
LOGDIR.mkdir(parents=True, exist_ok=True)

PY = str(APPDIR/".venv"/"bin"/"python")
if not Path(PY).exists():
    PY = sys.executable

def free_port(start):
    p = start
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
        p += 1

LIC_PORT  = free_port(int(os.getenv("KES_LICENSE_PORT",  "8787")))
TERM_PORT = free_port(int(os.getenv("KES_TERMINAL_PORT", "8788")))

with open(LOGDIR/"ports.env","w") as f:
    f.write(f"export KES_LICENSE_PORT={LIC_PORT}\nexport KES_TERMINAL_PORT={TERM_PORT}\n")

env = os.environ.copy()
env.update({
  "FLASK_ENV": "production",
  "KES_LICENSE_HOST": "127.0.0.1",
  "KES_LICENSE_PORT":  str(LIC_PORT),
  "KES_TERMINAL_HOST": "127.0.0.1",
  "KES_TERMINAL_PORT": str(TERM_PORT),
})

procs = []
def spawn(script, logname):
    lf = open(LOGDIR/logname, "a", buffering=1)
    p = subprocess.Popen([PY, str(APPDIR/script)], cwd=str(APPDIR), env=env,
                         stdout=lf, stderr=lf, text=True)
    procs.append((p, lf))

def main():
    spawn(Path("webui")/"license_server.py",  "license.log")
    spawn(Path("webui")/"terminal-server.py", "terminal.log")
    while True:
        if not all(p.poll() is None for p,_ in procs):
            break
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    finally:
        for p, lf in procs:
            try:
                p.terminate(); p.wait(timeout=5)
            except Exception:
                try: p.kill()
                except Exception: pass
            try: lf.close()
            except Exception: pass
