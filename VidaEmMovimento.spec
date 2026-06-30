# VidaEmMovimento.spec
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

mediapipe_datas = collect_data_files("mediapipe")
mediapipe_bins  = collect_dynamic_libs("mediapipe")

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[] + mediapipe_bins,
    datas=[
        ("assets", "assets"),
        ("pose_landmarker_full.task", "."),
    ] + mediapipe_datas,
    hiddenimports=[
        "mediapipe",
        "mediapipe.python",
        "mediapipe.python.solutions",
        "mediapipe.tasks",
        "mediapipe.tasks.python",
        "mediapipe.tasks.python.vision",
        "cv2",
        "numpy",
        "PySide6",
        "PySide6.QtWidgets",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtMultimedia",
        "PySide6.QtMultimediaWidgets",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VidaEmMovimento",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="VidaEmMovimento",
)
