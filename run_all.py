# run_all.py
import subprocess
import sys
import os

def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("app", exist_ok=True)
    
    print("\n" + "="*60)
    print(" INVESTIQ PRO - INSTALLER & RUNNER ")
    print("="*60 + "\n")
    
    # Install packages
    packages = ['yfinance', 'pandas', 'numpy', 'ta', 'streamlit', 'plotly', 'requests']
    for pkg in packages:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg])
        print(f"[✓] {pkg}")
    
    # Run fetchers
    print("\n[>] Fetching data...")
    subprocess.run([sys.executable, "-c", 
        "from app.data.fetcher import update_all; update_all()"])
    
    print("\n[✓] All done. Starting dashboard...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])

if __name__ == "__main__":
    main()