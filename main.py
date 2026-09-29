from ai.story import StoryGenerator
from utils.files import create_project_folder, save_scene_plan


def main():

    print("=" * 50)
    print("             STORYFORGE AI")
    print("=" * 50)

    story = input("\nEnter your story:\n> ")

    if not story.strip():
        print("Story cannot be empty.")
        return

    print("\nAnalyzing story...")

    try:
        generator = StoryGenerator()
        # scene_plan = generator.generate_scene_plan(story)
        scene_plan = generator.generate_scene_plan(story,target_duration=30)

        print("\nStory analysis completed!")

        # Create project folder
        project_dir = create_project_folder(
            scene_plan["title"]
        )

        # Save scene plan
        scene_file = save_scene_plan(
            project_dir,
            scene_plan
        )

        print(f"\nTitle: {scene_plan['title']}")

        print("\nScenes:")

        for scene in scene_plan["scenes"]:
            print(
                f"\nScene {scene['scene_id']}"
                f" | {scene['duration']} seconds"
            )

            print(f"Visual: {scene['visual_prompt']}")
            print(f"Narration: {scene['narration']}")

        print("\n" + "=" * 50)
        print("Scene plan saved successfully!")
        print(f"Location: {scene_file}")
        print("=" * 50)

    except Exception as e:
        print(f"\nERROR: {e}")


if __name__ == "__main__":
    main()