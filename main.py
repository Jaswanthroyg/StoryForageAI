from pathlib import Path

from ai.story import StoryGenerator
from ai.image import ImageGenerator
from ai.audio import AudioGenerator

from utils.files import (
    create_project_folder,
    save_scene_plan
)

from video.composer import VideoComposer
from video.merge import VideoMerger


def main():

    print("=" * 60)
    print("                    STORYFORGE AI")
    print("=" * 60)

    # --------------------------------------------------
    # 1. GET STORY
    # --------------------------------------------------

    story = input("\nEnter your story:\n> ")

    if not story.strip():
        print("\n❌ Story cannot be empty.")
        return

    # --------------------------------------------------
    # 2. STORY GENERATION
    # --------------------------------------------------

    try:

        print("\n" + "=" * 60)
        print("STEP 1: ANALYZING STORY")
        print("=" * 60)

        story_generator = StoryGenerator()

        scene_plan = story_generator.generate_scene_plan(
            story,
            target_duration=30
        )

        print("\n✅ Story analysis completed!")

    except Exception as e:

        print("\n❌ STORY GENERATION FAILED")
        print(f"Reason: {e}")
        return

    # --------------------------------------------------
    # 3. CREATE PROJECT FOLDER
    # --------------------------------------------------

    try:

        project_dir = create_project_folder(
            scene_plan["title"]
        )

        print(f"\nProject folder: {project_dir}")

        scene_file = save_scene_plan(
            project_dir,
            scene_plan
        )

        print(f"Scene plan saved: {scene_file}")

    except Exception as e:

        print("\n❌ PROJECT SETUP FAILED")
        print(f"Reason: {e}")
        return

    # --------------------------------------------------
    # 4. DISPLAY SCENE PLAN
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("GENERATED SCENES")
    print("=" * 60)

    for scene in scene_plan["scenes"]:

        print(
            f"\nScene {scene['scene_id']}"
            f" | Duration: {scene['duration']} seconds"
        )

        print(
            f"Visual: "
            f"{scene['visual_prompt']}"
        )

        print(
            f"Narration: "
            f"{scene['narration']}"
        )

    # --------------------------------------------------
    # 5. IMAGE GENERATION
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 2: GENERATING SCENE IMAGES")
    print("=" * 60)

    images_dir = project_dir / "images"
    images_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    image_generator = ImageGenerator()

    for scene in scene_plan["scenes"]:

        scene_number = scene["scene_id"]

        image_path = (
            images_dir /
            f"scene_{scene_number:02d}.png"
        )

        try:

            print(
                f"\nGenerating image "
                f"for Scene {scene_number}..."
            )

            image_generator.generate_image(
                scene["visual_prompt"],
                str(image_path)
            )

        except Exception as e:

            print(
                f"\n❌ IMAGE GENERATION FAILED "
                f"FOR SCENE {scene_number}"
            )

            print(f"Reason: {e}")
            return

    print("\n✅ All scene images generated successfully!")

    # --------------------------------------------------
    # 6. AUDIO GENERATION
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 3: GENERATING NARRATION")
    print("=" * 60)

    audio_dir = project_dir / "audio"
    audio_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    audio_generator = AudioGenerator()

    for scene in scene_plan["scenes"]:

        scene_number = scene["scene_id"]

        audio_path = (
            audio_dir /
            f"scene_{scene_number:02d}.mp3"
        )

        try:

            print(
                f"\nGenerating narration "
                f"for Scene {scene_number}..."
            )

            audio_generator.generate_audio(
                scene["narration"],
                str(audio_path)
            )

        except Exception as e:

            print(
                f"\n❌ AUDIO GENERATION FAILED "
                f"FOR SCENE {scene_number}"
            )

            print(f"Reason: {e}")
            return

    print("\n✅ All narration audio generated successfully!")

    # --------------------------------------------------
    # 7. CREATE SCENE VIDEOS
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 4: CREATING SCENE VIDEOS")
    print("=" * 60)

    videos_dir = project_dir / "videos"
    videos_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    video_composer = VideoComposer()
    scene_videos = []

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

        video_path = (
            videos_dir /
            f"scene_{scene_number:02d}.mp4"
        )

        try:

            print(
                f"\nCreating video "
                f"for Scene {scene_number}..."
            )

            video_composer.create_scene_video(
                str(image_path),
                str(audio_path),
                str(video_path),
                duration
            )

            scene_videos.append(video_path)

        except Exception as e:

            print(
                f"\n❌ VIDEO CREATION FAILED "
                f"FOR SCENE {scene_number}"
            )

            print(f"Reason: {e}")
            return

    print("\n✅ All scene videos created successfully!")

    # --------------------------------------------------
    # 8. MERGE + BACKGROUND MUSIC
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 5: CREATING FINAL VIDEO")
    print("=" * 60)

    try:

        music_path = Path(
            "music/background.mp3"
        )

        video_merger = VideoMerger(
            music_path
        )

        final_video = video_merger.merge_scene_videos(
            project_dir,
            scene_videos,
            output_filename=(
                f"{scene_plan['title']}_final.mp4"
            )
        )

    except Exception as e:

        print("\n❌ FINAL VIDEO CREATION FAILED")
        print(f"Reason: {e}")
        return

    # --------------------------------------------------
    # 9. COMPLETED
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("          STORYFORGE AI COMPLETED!")
    print("=" * 60)

    print(f"\nTitle: {scene_plan['title']}")

    print(
        f"\nFinal video:\n"
        f"{final_video}"
    )

    print("\n🎬 Your video is ready!")


if __name__ == "__main__":
    main()