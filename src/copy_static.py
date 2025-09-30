import os
import shutil

def copy_static(src='static', dst='docs'):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.makedirs(dst, exist_ok=True)

    for root, dirs, files in os.walk(src):
        # Compute destination path
        rel_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dst, rel_path) if rel_path != '.' else dst

        # Make subdirectories
        for d in dirs:
            os.makedirs(os.path.join(dest_dir, d), exist_ok=True)

        # Copy files
        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(dest_dir, f)
            shutil.copy(src_file, dst_file)
            print(f'Copied {src_file} -> {dst_file}')

if __name__ == '__main__':
    copy_static()

