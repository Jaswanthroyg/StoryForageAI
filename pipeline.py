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


class StoryForgePipeline:

    def __init__(self):

        self.story_generator = StoryGenerator()
        self.image_generator = ImageGenerator()
        self.audio_generator = AudioGenerator()
        self.video_composer = VideoComposer()

        self.music_path = Path(
            "music/background.mp3"
        )

    def run(self, story, target_duration=30):

        # ------------------------------------------
        # 1. STORY GENERATION
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("STEP 1: ANALYZING STORY")
        print("=" * 60)

        try:

            scene_plan = (
                self.story_generator
                .generate_scene_plan(
                    story,
                    target_duration=target_duration
                )
            )

            print("\n✅ Story analysis completed!")

        except Exception as e:

            print("\n❌ STORY GENERATION FAILED")
            print(f"Reason: {e}")
            return None

        # ------------------------------------------
        # 2. PROJECT SETUP
        # ------------------------------------------

        try:

            project_dir = create_project_folder(
                scene_plan["title"]
            )

            print(
                f"\nProject folder: "
                f"{project_dir}"
            )

            scene_file = save_scene_plan(
                project_dir,
                scene_plan
            )

            print(
                f"Scene plan saved: "
                f"{scene_file}"
            )

        except Exception as e:

            print("\n❌ PROJECT SETUP FAILED")
            print(f"Reason: {e}")
            return None

        total_scenes = len(
            scene_plan["scenes"]
        )

        # ------------------------------------------
        # 3. DISPLAY SCENE PLAN
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("GENERATED SCENES")
        print("=" * 60)

        for scene in scene_plan["scenes"]:

            print(
                f"\nScene {scene['scene_id']}"
                f" | Duration: "
                f"{scene['duration']} seconds"
            )

            print(
                f"Visual: "
                f"{scene['visual_prompt']}"
            )

            print(
                f"Narration: "
                f"{scene['narration']}"
            )

        # ------------------------------------------
        # 4. IMAGE GENERATION
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("STEP 2: GENERATING SCENE IMAGES")
        print("=" * 60)

        images_dir = project_dir / "images"

        images_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for scene in scene_plan["scenes"]:

            scene_number = scene["scene_id"]

            image_path = (
                images_dir /
                f"scene_{scene_number:02d}.png"
            )

            try:

                print(
                    f"\n[Image Generation] "
                    f"Scene "
                    f"{scene_number}/"
                    f"{total_scenes}"
                )

                self.image_generator.generate_image(
                    scene["visual_prompt"],
                    str(image_path)
                )

                print(
                    f"✅ Scene "
                    f"{scene_number}/"
                    f"{total_scenes} completed"
                )

            except Exception as e:

                print(
                    f"\n❌ IMAGE GENERATION "
                    f"FAILED FOR SCENE "
                    f"{scene_number}"
                )

                print(f"Reason: {e}")
                return None

        print(
            "\n✅ All scene images "
            "generated successfully!"
        )

        # ------------------------------------------
        # 5. AUDIO GENERATION
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("STEP 3: GENERATING NARRATION")
        print("=" * 60)

        audio_dir = project_dir / "audio"

        audio_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for scene in scene_plan["scenes"]:

            scene_number = scene["scene_id"]

            audio_path = (
                audio_dir /
                f"scene_{scene_number:02d}.mp3"
            )

            try:

                print(
                    f"\n[Audio Generation] "
                    f"Scene "
                    f"{scene_number}/"
                    f"{total_scenes}"
                )

                self.audio_generator.generate_audio(
                    scene["narration"],
                    str(audio_path)
                )

                print(
                    f"✅ Scene "
                    f"{scene_number}/"
                    f"{total_scenes} completed"
                )

            except Exception as e:

                print(
                    f"\n❌ AUDIO GENERATION "
                    f"FAILED FOR SCENE "
                    f"{scene_number}"
                )

                print(f"Reason: {e}")
                return None

        print(
            "\n✅ All narration audio "
            "generated successfully!"
        )

        # ------------------------------------------
        # 6. CREATE SCENE VIDEOS
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("STEP 4: CREATING SCENE VIDEOS")
        print("=" * 60)

        videos_dir = project_dir / "videos"

        videos_dir.mkdir(
            parents=True,
            exist_ok=True
        )

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
                    f"\n[Video Creation] "
                    f"Scene "
                    f"{scene_number}/"
                    f"{total_scenes}"
                )

                self.video_composer.create_scene_video(
                    str(image_path),
                    str(audio_path),
                    str(video_path),
                    duration
                )

                scene_videos.append(video_path)

                print(
                    f"✅ Scene "
                    f"{scene_number}/"
                    f"{total_scenes} completed"
                )

            except Exception as e:

                print(
                    f"\n❌ VIDEO CREATION "
                    f"FAILED FOR SCENE "
                    f"{scene_number}"
                )

                print(f"Reason: {e}")
                return None

        print(
            "\n✅ All scene videos "
            "created successfully!"
        )

        # ------------------------------------------
        # 7. MERGE + BACKGROUND MUSIC
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("STEP 5: CREATING FINAL VIDEO")
        print("=" * 60)

        try:

            video_merger = VideoMerger(
                self.music_path
            )

            final_video = (
                video_merger.merge_scene_videos(
                    project_dir,
                    scene_videos,
                    output_filename=(
                        f"{scene_plan['title']}"
                        "_final.mp4"
                    )
                )
            )

        except Exception as e:

            print(
                "\n❌ FINAL VIDEO "
                "CREATION FAILED"
            )

            print(f"Reason: {e}")
            return None

        # ------------------------------------------
        # 8. RETURN RESULT
        # ------------------------------------------

        return {
            "title": scene_plan["title"],
            "project_dir": project_dir,
            "scene_plan": scene_plan,
            "final_video": final_video
        }