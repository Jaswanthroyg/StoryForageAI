import json
from pathlib import Path

from video.composer import VideoComposer


project_dir = Path("output/Wings_of_the_Village")

images_dir = project_dir / "images"
audio_dir = project_dir / "audio"
videos_dir = project_dir / "videos"

videos_dir.mkdir(parents=True, exist_ok=True)


# Read scene plan
scene_plan_file = project_dir / "scenes.json"

with open(scene_plan_file, "r", encoding="utf-8") as file:
    scene_plan = json.load(file)


composer = VideoComposer()


for scene in scene_plan["scenes"]:

    scene_number = scene["scene_id"]
    duration = scene["duration"]

    image_path = (
        images_dir /
        f"scene_{scene_number:02d}.png"
    )

    audio_path = (
        audio_dir /
        f"scene_{scene_number:02d}.mp3"
    )

    output_path = (
        videos_dir /
        f"scene_{scene_number:02d}.mp4"
    )

    print()
    print("=" * 50)
    print(f"Creating Scene {scene_number}")
    print(f"Target duration: {duration} seconds")
    print("=" * 50)

    composer.create_scene_video(
        image_path,
        audio_path,
        output_path,
        duration=duration
    )


print()
print("========================================")
print("All scene videos created successfully!")
print("========================================")