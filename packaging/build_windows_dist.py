import os
import sys
import shutil
import hashlib
import subprocess
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
frontend_dir = root_dir / "frontend"
dist_dir = root_dir / "dist"
release_dir = root_dir / "release"

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

def main():
    print("==================================================")
    print("NUGI CONTENT FACTORY — WINDOWS PACKAGING PIPELINE")
    print("==================================================")

    # 1. Build Frontend
    print("\n[Step 1/5] Building Frontend Production Bundle (Vite)...")
    res = subprocess.run("npm run build", shell=True, cwd=str(frontend_dir))
    if res.returncode != 0:
        print("ERROR: Frontend build failed.")
        sys.exit(1)

    # 2. Run PyInstaller
    print("\n[Step 2/5] Compiling Desktop Application via PyInstaller...")
    spec_path = root_dir / "packaging" / "desktop.spec"
    res = subprocess.run(f"pyinstaller --noconfirm {spec_path}", shell=True, cwd=str(root_dir))
    if res.returncode != 0:
        print("ERROR: PyInstaller packaging failed.")
        sys.exit(1)

    # 3. Create Portable Zip
    print("\n[Step 3/5] Creating Portable Distribution Zip Archive...")
    release_dir.mkdir(parents=True, exist_ok=True)
    app_folder = dist_dir / "Nugi Content Factory"
    portable_zip = release_dir / "Nugi-Content-Factory-Windows-x64-Portable.zip"
    
    if app_folder.exists():
        if portable_zip.exists():
            portable_zip.unlink()
        shutil.make_archive(
            base_name=str(release_dir / "Nugi-Content-Factory-Windows-x64-Portable"),
            format="zip",
            root_dir=str(dist_dir),
            base_dir="Nugi Content Factory"
        )
        print(f"Portable package created: {portable_zip} ({portable_zip.stat().st_size / (1024*1024):.2f} MB)")

    # 4. Compile Inno Setup (if iscc is available)
    print("\n[Step 4/5] Compiling Inno Setup Windows Installer...")
    iss_file = root_dir / "packaging" / "installer.iss"
    
    iscc_candidates = [
        shutil.which("iscc"),
        str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Inno Setup 6" / "ISCC.exe"),
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    iscc_cmd = next((p for p in iscc_candidates if p and os.path.exists(p)), None)
    
    if iscc_cmd:
        print(f"Found Inno Setup Compiler at: {iscc_cmd}")
        res = subprocess.run(f'"{iscc_cmd}" "{iss_file}"', shell=True)
        if res.returncode == 0:
            setup_exe = release_dir / "Nugi-Content-Factory-Windows-x64-Setup.exe"
            if setup_exe.exists():
                print(f"Installer created: {setup_exe} ({setup_exe.stat().st_size / (1024*1024):.2f} MB)")
            else:
                print("WARNING: ISCC exited 0 but setup_exe not found.")
        else:
            print("ERROR: ISCC compilation failed.")
            sys.exit(1)
    else:
        print("NOTE: Inno Setup (ISCC) not detected in local path; skipping installer compilation (will be built in GitHub Actions).")

    # 5. Generate Checksums
    print("\n[Step 5/5] Generating SHA256 Checksums...")
    checksum_file = release_dir / "SHA256SUMS.txt"
    with open(checksum_file, "w", encoding="utf-8") as f:
        for p in release_dir.iterdir():
            if p.is_file() and p.name != "SHA256SUMS.txt":
                h = compute_sha256(p)
                f.write(f"{h}  {p.name}\n")
                print(f"SHA256 ({p.name}) = {h}")

    print("\n==================================================")
    print("PACKAGING PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Output directory: {release_dir}")
    print("==================================================")

if __name__ == "__main__":
    main()
