# run_all.py  ->  python run_all.py
"""
Installer + runner satu pintu untuk Ridho Capital.

  python run_all.py                  pasang paket yang belum ada, lalu jalankan dashboard
  python run_all.py --update-data    ikut memperbarui database fundamental, emas, dan proyeksi (lambat)
  python run_all.py --skip-install   langsung jalankan dashboard
  python run_all.py --port 8502      pakai port lain
  python run_all.py --check          hanya periksa paket dan file, tanpa menjalankan dashboard
"""
import argparse
import importlib.util
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# (nama paket pip, nama modul untuk dicek)
PACKAGES = [
    ("streamlit>=1.50", "streamlit"),   # st.pills & st.popover butuh versi ini
    ("yfinance", "yfinance"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("ta", "ta"),
    ("plotly", "plotly"),
    ("requests", "requests"),
    ("python-dotenv", "dotenv"),
]
REQUIRED_FILES = ["dashboard.py", "app/utils/config.py", "app/core/horizon.py", "app/ui/views.py", "app/data/market.py"]


def banner(text):
    print("\n" + "=" * 60 + f"\n {text}\n" + "=" * 60)


def streamlit_ok():
    """True jika streamlit terpasang dan versinya >= 1.50."""
    if importlib.util.find_spec("streamlit") is None:
        return False
    try:
        from importlib.metadata import version
        major, minor = (int(x) for x in version("streamlit").split(".")[:2])
        return (major, minor) >= (1, 50)
    except Exception:
        return False


def install_packages():
    banner("Memeriksa paket")
    for spec, module in PACKAGES:
        ok = streamlit_ok() if module == "streamlit" else importlib.util.find_spec(module) is not None
        if ok:
            print(f"[✓] {spec} sudah terpasang")
            continue
        print(f"[>] Memasang {spec} ...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", spec])
        print(f"[{'✓' if r.returncode == 0 else '✗'}] {spec}")
        if r.returncode != 0:
            sys.exit(f"Gagal memasang {spec}. Periksa koneksi internet lalu coba lagi.")


def check_files():
    missing = [f for f in REQUIRED_FILES if not os.path.exists(os.path.join(ROOT, f))]
    if missing:
        sys.exit("File berikut tidak ditemukan:\n  - " + "\n  - ".join(missing)
                 + "\nJalankan run_all.py dari folder proyek yang lengkap.")


def update_data():
    banner("Memperbarui data (bisa memakan beberapa menit)")
    code = ("from app.data.fetcher import update_all; update_all();"
            "from app.models.forecast import update_forecasts; update_forecasts()")
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT)
    print("[✓] Data diperbarui" if r.returncode == 0 else "[!] Sebagian data gagal diperbarui, dashboard tetap bisa dipakai")


def main():
    ap = argparse.ArgumentParser(description="Installer dan runner Ridho Capital")
    ap.add_argument("--skip-install", action="store_true", help="lewati pemasangan paket")
    ap.add_argument("--update-data", action="store_true", help="perbarui database fundamental, emas, proyeksi")
    ap.add_argument("--port", type=int, default=8501, help="port dashboard (default 8501)")
    ap.add_argument("--check", action="store_true", help="hanya periksa, jangan jalankan dashboard")
    args = ap.parse_args()

    os.chdir(ROOT)
    os.makedirs("data", exist_ok=True)
    banner("RIDHO CAPITAL - INSTALLER & RUNNER")

    check_files()
    if not args.skip_install:
        install_packages()
    if args.check:
        print("\n[✓] Semua file dan paket siap.")
        return
    if args.update_data:
        update_data()

    banner(f"Menjalankan dashboard di http://localhost:{args.port}")
    print("Tekan Ctrl+C untuk berhenti.\n")
    env = dict(os.environ, PYTHONPATH=ROOT + os.pathsep + os.environ.get("PYTHONPATH", ""))
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py",
                        "--server.port", str(args.port), "--browser.gatherUsageStats", "false"],
                       cwd=ROOT, env=env)
    except KeyboardInterrupt:
        print("\n[✓] Dashboard dihentikan.")


if __name__ == "__main__":
    main()
