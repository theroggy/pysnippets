    from pathlib import Path
    import shutil

    src_dir = Path("C:/temp/test_recursivecopy/src")
    dst_dir = Path("C:/temp/test_recursivecopy/dst")

    files = src_dir.glob("**/*.geojson")
    for file in files:
        shutil.copy(file, dst_dir)
