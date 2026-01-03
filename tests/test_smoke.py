#smoke test sprawdzający, czy aplikacja Streamlit
#potrafi się uruchomić bez natychmiastowego błędu

import subprocess
import sys
import time
import os

def test_smoke_streamlit_starts(tmp_path):
    """Smoke test: start Streamlit briefly to ensure the app can start.

    The process is started and allowed to run for a short period. The test
    asserts the process did not immediately exit with an error and then
    terminates it.
    """
    cwd = os.getcwd()

    port = "8502"
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "main.py", "--server.headless", "true", "--server.port", port],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        time.sleep(3)
        assert proc.poll() is None
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        out, err = proc.communicate(timeout=1)
        assert "Traceback" not in err
