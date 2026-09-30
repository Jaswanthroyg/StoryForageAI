from pipeline import StoryForgePipeline


def main():

    print("=" * 60)
    print("                    STORYFORGE AI")
    print("=" * 60)

    story = input("\nEnter your story:\n> ")

    if not story.strip():

        print("\n❌ Story cannot be empty.")
        return

    pipeline = StoryForgePipeline()

    result = pipeline.run(
        story,
        target_duration=30
    )

    if result is None:

        print("\nStoryForge stopped.")
        return

    print("\n" + "=" * 60)
    print("          STORYFORGE AI COMPLETED!")
    print("=" * 60)

    print(
        f"\nTitle: "
        f"{result['title']}"
    )

    print(
        f"\nFinal video:\n"
        f"{result['final_video']}"
    )

    print("\n🎬 Your video is ready!")


if __name__ == "__main__":
    main()