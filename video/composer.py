import subprocess


class VideoComposer:

    def create_scene_video(
        self,
        image_path,
        audio_path,
        output_path,
        duration
    ):

        command = [
            "ffmpeg",
            "-y",

            # Image
            "-loop", "1",
            "-i", image_path,

            # Narration
            "-i", audio_path,

            # Video
            "-map", "0:v:0",
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-pix_fmt", "yuv420p",

            # Audio
            "-map", "1:a:0",
            "-c:a", "aac",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "128k",

            # Exact scene duration
            "-t", str(duration),

            "-movflags", "+faststart",

            output_path
        ]

        subprocess.run(
            command,
            check=True
        )

        print("Scene video created successfully!")