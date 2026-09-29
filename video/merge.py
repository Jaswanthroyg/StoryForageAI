import subprocess
from pathlib import Path


# ==========================================
# Paths
# ==========================================

project_dir = Path("output/Wings_of_the_Village")

videos_dir = project_dir / "videos"

music_path = Path("music/background.mp3")

final_video = (
    project_dir /
    "Wings_of_the_Village_final_with_music.mp4"
)

concat_file = (
    project_dir /
    "concat.txt"
)


# ==========================================
# Scene videos
# ==========================================

scene_videos = [
    videos_dir / "scene_01.mp4",
    videos_dir / "scene_02.mp4",
    videos_dir / "scene_03.mp4",
    videos_dir / "scene_04.mp4",
    videos_dir / "scene_05.mp4",
]


# ==========================================
# Create FFmpeg concat file
# ==========================================

with open(concat_file, "w", encoding="utf-8") as file:

    for video in scene_videos:

        file.write(
            f"file '{video.resolve()}'\n"
        )


# ==========================================
# FFmpeg command
# ==========================================

command = [

    "ffmpeg",
    "-y",

    # --------------------------------------
    # Input 0: all scene videos
    # --------------------------------------

    "-f", "concat",
    "-safe", "0",
    "-i", str(concat_file),

    # --------------------------------------
    # Input 1: background music
    # Loop music so it covers the video
    # --------------------------------------

    "-stream_loop", "-1",
    "-i", str(music_path),

    # --------------------------------------
    # Keep the concatenated video
    # --------------------------------------

    "-map", "0:v:0",

    # --------------------------------------
    # Mix:
    #
    # 0:a = narration
    # 1:a = background music
    #
    # Music volume = 15%
    # --------------------------------------

    "-filter_complex",

    (
        "[1:a]"
        "volume=0.15"
        "[music];"

        "[0:a][music]"
        "amix="
        "inputs=2:"
        "duration=first:"
        "dropout_transition=2"
        "[audio]"
    ),

    # --------------------------------------
    # Video
    # --------------------------------------

    "-c:v", "copy",

    # --------------------------------------
    # Mixed audio
    # --------------------------------------

    "-map", "[audio]",

    "-c:a", "aac",
    "-ar", "44100",
    "-ac", "2",
    "-b:a", "192k",

    # --------------------------------------
    # Final duration
    # --------------------------------------

    "-t", "30.02",

    # --------------------------------------
    # Better MP4 playback
    # --------------------------------------

    "-movflags", "+faststart",

    str(final_video)
]


# ==========================================
# Run FFmpeg
# ==========================================

print()
print("======================================")
print("Creating final StoryForge video...")
print("======================================")
print()

subprocess.run(
    command,
    check=True
)

print()
print("======================================")
print("FINAL VIDEO CREATED SUCCESSFULLY!")
print("======================================")
print()
print(f"Output: {final_video}")