import subprocess
import sys
import time
import os


def test_smoke_streamlit_starts(tmp_path):
    """Start Streamlit app process and verify it stays alive for a moment."""

    ####### changes made with help of ChatGPT #######
    env = os.environ.copy()
    env["TDL_DB_PATH"] = str(tmp_path / "smoke.db")

    port = "8502"

    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/main.py",
            "--server.headless=true",
            f"--server.port={port}",
            "--server.address=127.0.0.1",
        ],
        cwd=os.getcwd(),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    #################################################

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
