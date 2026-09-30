import subprocess
from pathlib import Path


class VideoMerger:

    def __init__(self, music_path):
        self.music_path = Path(music_path)

    def merge_scene_videos(
        self,
        project_dir,
        scene_videos,
        output_filename="final_video.mp4"
    ):

        project_dir = Path(project_dir)

        final_video = project_dir / output_filename

        concat_file = project_dir / "concat.txt"

        # Create FFmpeg concat file
        with open(
            concat_file,
            "w",
            encoding="utf-8"
        ) as file:

            for video in scene_videos:
                file.write(
                    f"file '{Path(video).resolve()}'\n"
                )

        command = [
            "ffmpeg",
            "-y",

            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),

            "-stream_loop", "-1",
            "-i", str(self.music_path),

            "-map", "0:v:0",

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

            "-c:v", "copy",

            "-map", "[audio]",

            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "192k",

            "-movflags", "+faststart",

            str(final_video)
        ]

        print("\nCreating final StoryForge video...")

        subprocess.run(
            command,
            check=True
        )

        print("\nFinal video created successfully!")
        print(f"\nOutput: {final_video}")

        return final_video