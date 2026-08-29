#!/usr/bin/env python3
"""按画面相似度查找重复视频，并保留每组中最大的文件。需要 FFmpeg。"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


VIDEO_EXTS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
    ".m4v", ".mpg", ".mpeg", ".ts", ".mts", ".m2ts", ".3gp",
}
HASH_SIZE = 16
FRAME_COUNT = 12


@dataclass
class Video:
    path: Path
    size: int
    duration: float
    width: int
    height: int
    hashes: list[int]


def run(command: list[str]) -> bytes:
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def inspect_video(path: Path) -> Video:
    raw = run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height:format=duration",
        "-of", "json", str(path),
    ])
    data = json.loads(raw)
    stream = data["streams"][0]
    duration = float(data["format"].get("duration") or 0)
    if duration <= 0:
        raise ValueError("无法读取视频时长")

    # 取视频中间 90% 的均匀样本，避开容易变化的片头和片尾。
    fps = FRAME_COUNT / (duration * 0.9)
    frames = run([
        "ffmpeg", "-v", "error", "-ss", f"{duration * 0.05:.3f}",
        "-i", str(path), "-t", f"{duration * 0.9:.3f}",
        "-vf", f"fps={fps:.8f},scale={HASH_SIZE}:{HASH_SIZE},format=gray",
        "-frames:v", str(FRAME_COUNT), "-f", "rawvideo", "-",
    ])
    pixels_per_frame = HASH_SIZE * HASH_SIZE
    hashes = []
    for start in range(0, len(frames), pixels_per_frame):
        pixels = frames[start:start + pixels_per_frame]
        if len(pixels) != pixels_per_frame:
            continue
        mean = sum(pixels) / pixels_per_frame
        hashes.append(sum((pixel >= mean) << i for i, pixel in enumerate(pixels)))
    if len(hashes) < max(4, FRAME_COUNT // 2):
        raise ValueError("可读取的画面太少")
    return Video(path, path.stat().st_size, duration, int(stream["width"]),
                 int(stream["height"]), hashes)


def distance(a: Video, b: Video) -> float:
    count = min(len(a.hashes), len(b.hashes))
    values = [
        (a.hashes[i] ^ b.hashes[i]).bit_count() / (HASH_SIZE * HASH_SIZE)
        for i in range(count)
    ]
    values.sort()
    return values[len(values) // 2]


def find_groups(videos: list[Video], threshold: float,
                duration_tolerance: float) -> list[list[Video]]:
    parent = list(range(len(videos)))

    def root(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        a, b = root(a), root(b)
        if a != b:
            parent[b] = a

    for i, a in enumerate(videos):
        for j in range(i + 1, len(videos)):
            b = videos[j]
            relative_duration_gap = abs(a.duration - b.duration) / max(a.duration, b.duration)
            if relative_duration_gap <= duration_tolerance and distance(a, b) <= threshold:
                union(i, j)

    groups: dict[int, list[Video]] = {}
    for i, video in enumerate(videos):
        groups.setdefault(root(i), []).append(video)
    return [sorted(group, key=lambda video: video.size, reverse=True)
            for group in groups.values() if len(group) > 1]


def unique_destination(folder: Path, source: Path) -> Path:
    candidate = folder / source.name
    number = 1
    while candidate.exists():
        candidate = folder / f"{source.stem}_{number}{source.suffix}"
        number += 1
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="要扫描的视频文件夹")
    parser.add_argument("--move", action="store_true",
                        help="把较小的重复文件移入 _video_duplicates 文件夹")
    parser.add_argument("--threshold", type=float, default=0.16,
                        help="画面差异阈值，越大越宽松，默认 0.16")
    parser.add_argument("--duration-tolerance", type=float, default=0.03,
                        help="允许的时长比例差，默认 0.03")
    args = parser.parse_args()
    folder = args.folder.resolve()
    if not folder.is_dir():
        parser.error(f"文件夹不存在：{folder}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("未找到 FFmpeg。请先安装 FFmpeg，并确保 ffmpeg 和 ffprobe 可用。")

    quarantine = folder / "_video_duplicates"
    paths = [path for path in folder.rglob("*")
             if path.is_file() and path.suffix.lower() in VIDEO_EXTS
             and quarantine not in path.parents]
    videos: list[Video] = []
    print(f"找到 {len(paths)} 个视频，正在分析画面……")
    for number, path in enumerate(paths, 1):
        try:
            videos.append(inspect_video(path))
            print(f"[{number}/{len(paths)}] {path.name}")
        except Exception as error:
            print(f"[跳过] {path}: {error}", file=sys.stderr)

    groups = find_groups(videos, args.threshold, args.duration_tolerance)
    report = folder / "video_duplicates.csv"
    with report.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["组", "处理", "文件", "大小MB", "时长秒", "分辨率"])
        for group_number, group in enumerate(groups, 1):
            for index, video in enumerate(group):
                writer.writerow([
                    group_number, "保留" if index == 0 else "重复",
                    str(video.path), f"{video.size / 1024 / 1024:.2f}",
                    f"{video.duration:.2f}", f"{video.width}x{video.height}",
                ])

    duplicate_count = sum(len(group) - 1 for group in groups)
    print(f"\n发现 {len(groups)} 组相似视频，共 {duplicate_count} 个较小的重复文件。")
    print(f"报告：{report}")
    if args.move and duplicate_count:
        quarantine.mkdir(exist_ok=True)
        for group in groups:
            for video in group[1:]:
                destination = unique_destination(quarantine, video.path)
                shutil.move(str(video.path), destination)
                print(f"已移动：{video.path} -> {destination}")
        print(f"较小文件已移入：{quarantine}")
    elif duplicate_count:
        print("当前只是检查。确认报告后，加 --move 再运行即可移动重复文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
