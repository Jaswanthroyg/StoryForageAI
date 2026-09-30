from google import genai
from dotenv import load_dotenv
import os
import json
from utils.retry import retry_operation

load_dotenv()


class StoryGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

    def generate_scene_plan(self, story, target_duration=30):

        prompt = f"""
You are the StoryForge AI story-to-video planning engine.

Convert the user's story into a cinematic video plan.

Target video duration: {target_duration} seconds.

Create a suitable number of scenes.

For every scene provide:

- scene_id
- duration
- visual_prompt
- narration

Rules:

1. Scenes must follow the story in chronological order.
2. Include only important moments from the story.
3. The total duration of all scenes MUST be exactly {target_duration} seconds.
4. The visual_prompt must clearly describe what should appear visually.
5. Make visual prompts cinematic and detailed.
6. Narration should naturally explain what is happening.
7. Return ONLY valid JSON.
8. Do not include markdown.
9. Do not include explanations outside the JSON.

Required JSON format:

{{
    "title": "Story title",
    "total_duration": {target_duration},
    "scenes": [
        {{
            "scene_id": 1,
            "duration": 6,
            "visual_prompt": "Detailed visual description",
            "narration": "Narration for this scene"
        }}
    ]
}}

USER STORY:

{story}
"""
        response = retry_operation(
            lambda: self.client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            ),
            operation_name="Gemini story Generation"
        )

        text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            scene_plan = json.loads(text)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Gemini returned invalid JSON: {e}\n\n"
                f"Response:\n{text}"
            )

        # Validate duration
        calculated_duration = sum(
            scene["duration"]
            for scene in scene_plan["scenes"]
        )

        if calculated_duration != target_duration:
            raise ValueError(
                f"Scene duration is {calculated_duration}s, "
                f"but target is {target_duration}s."
            )

        return scene_plan