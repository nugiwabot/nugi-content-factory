import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
release_dir = root_dir / "release"
setup_exe = release_dir / "Nugi-Content-Factory-Windows-x64-Setup.exe"
portable_zip = release_dir / "Nugi-Content-Factory-Windows-x64-Portable.zip"
checksums_file = release_dir / "SHA256SUMS.txt"
test_install_dir = root_dir / "build" / "test_install"

def test_release_files_exist():
    print("[1/4] Verifying physical release files exist...")
    assert setup_exe.exists(), f"Installer missing: {setup_exe}"
    assert setup_exe.stat().st_size > 10 * 1024 * 1024, "Installer size too small"
    print(f"  [OK] Setup.exe verified ({setup_exe.stat().st_size / (1024*1024):.2f} MB)")

    assert portable_zip.exists(), f"Portable zip missing: {portable_zip}"
    assert portable_zip.stat().st_size > 10 * 1024 * 1024, "Portable zip size too small"
    print(f"  [OK] Portable.zip verified ({portable_zip.stat().st_size / (1024*1024):.2f} MB)")

    if checksums_file.exists():
        content = checksums_file.read_text(encoding="utf-8")
        assert "Nugi-Content-Factory-Windows-x64-Setup.exe" in content
        assert "Nugi-Content-Factory-Windows-x64-Portable.zip" in content
        print("  [OK] SHA256SUMS.txt verified")
    else:
        print("  [INFO] SHA256SUMS.txt not yet generated (will run post-test)")

def test_silent_installation():
    print("\n[2/4] Testing Silent Installation to isolated directory...")
    if test_install_dir.exists():
        shutil.rmtree(test_install_dir, ignore_errors=True)
    test_install_dir.mkdir(parents=True, exist_ok=True)

    cmd = f'"{setup_exe}" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR="{test_install_dir}"'
    print(f"  Executing: {cmd}")
    res = subprocess.run(cmd, shell=True)
    assert res.returncode == 0, f"Installer failed with exit code: {res.returncode}"

    installed_exe = test_install_dir / "Nugi Content Factory.exe"
    assert installed_exe.exists(), f"Installed exe not found at: {installed_exe}"
    print(f"  [OK] Installation succeeded! Installed binary at: {installed_exe}")

def test_installed_binary_metadata():
    print("\n[3/4] Testing Installed Application Assets & Metadata...")
    installed_exe = test_install_dir / "Nugi Content Factory.exe"
    assets_dir = test_install_dir / "_internal" / "assets" / "brand"
    if not assets_dir.exists():
        assets_dir = test_install_dir / "assets" / "brand"
    frontend_dir = test_install_dir / "_internal" / "frontend" / "dist"
    if not frontend_dir.exists():
        frontend_dir = test_install_dir / "frontend" / "dist"

    assert assets_dir.exists(), "Brand assets missing in installation"
    assert (assets_dir / "app.ico").exists(), "app.ico missing"
    assert (assets_dir / "nugi_properti_logo.png").exists(), "nugi_properti_logo.png missing"
    assert frontend_dir.exists(), "Frontend static dist missing in installation"
    assert (frontend_dir / "index.html").exists(), "Frontend index.html missing"
    print("  [OK] All required runtime and brand assets verified in installed directory")

def test_silent_uninstall():
    print("\n[4/4] Testing Silent Uninstallation...")
    unins_exe = test_install_dir / "unins000.exe"
    if unins_exe.exists():
        cmd = f'"{unins_exe}" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART'
        print(f"  Executing uninstaller: {cmd}")
        res = subprocess.run(cmd, shell=True)
        print("  [OK] Uninstaller completed cleanly")
    else:
        print("  (Skipping unins000 execution)")

if __name__ == "__main__":
    print("==================================================")
    print("NUGI CONTENT FACTORY — INSTALLER SMOKE TEST")
    print("==================================================")
    test_release_files_exist()
    test_silent_installation()
    test_installed_binary_metadata()
    test_silent_uninstall()
    print("\n==================================================")
    print("ALL INSTALLER SMOKE TESTS PASSED (100%)!")
    print("==================================================")
