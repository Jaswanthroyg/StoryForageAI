import asyncio
import os

import edge_tts


class AudioGenerator:

    def __init__(
        self,
        voice="en-US-GuyNeural"
    ):
        self.voice = voice

    def generate_audio(
        self,
        text,
        output_path
    ):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        print("Generating narration...")

        asyncio.run(
            self._generate(
                text,
                output_path
            )
        )

        print("Narration saved successfully.")

        return output_path

    async def _generate(
        self,
        text,
        output_path
    ):

        communicate = edge_tts.Communicate(
            text,
            self.voice
        )

        await communicate.save(
            output_path
        )