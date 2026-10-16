"""Hero photo exports (RES-BRIEF, Oct 16, 2026): AVIF + WebP + JPEG at 800/1280/1600 px wide (never above the
source width: upscaling adds no detail) from the largest original in the repo. Output: photos/hero/<key>-<w>.<ext>.
Needs ffmpeg (libsvtav1, mjpeg) and cwebp. Source search and keep/drop decisions: HERO-RES.md.
    python3 tools/hero_images.py"""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {  # key: (original, width)
    'duo': ('photos/isb-2026/pitch-duo.jpg', 1600),
    'gesture': ('photos/isb-pitch-gesture.jpg', 1600),
    'mentors': ('photos/isb-2026/mentor-feedback.jpg', 1600),
    'laptop': ('photos/isb-judges-test.jpg', 1600),   # DEPTH-BRIEF: Technology hero
}
WIDTHS = (800, 1280, 1600)
OUT = os.path.join(ROOT, 'photos', 'hero')


def run(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    for key, (src, sw) in SRC.items():
        if only and key not in only:
            continue
        src = os.path.join(ROOT, src)
        for w in WIDTHS:
            if w > sw:
                continue
            base = os.path.join(OUT, '%s-%d' % (key, w))
            run('nice', 'ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=%d:-2:flags=lanczos,format=yuv420p' % w,
                '-c:v', 'libsvtav1', '-crf', '30', '-preset', '6', '-svtav1-params', 'tune=0', '-frames:v', '1', '-f', 'avif', base + '.avif')
            run('nice', 'ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=%d:-2:flags=lanczos' % w, '-q:v', '3', '-frames:v', '1', base + '.jpg')
            run('nice', 'cwebp', '-quiet', '-q', '80', '-m', '6', '-resize', str(w), '0', src, '-o', base + '.webp')
            print(key, w, *(os.path.getsize(base + e) // 1024 for e in ('.avif', '.webp', '.jpg')), 'KB')
