from pathlib import Path
import re
import json


def create_project_folder(title):
    """
    Creates a folder for the generated story.
    """

    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_title = safe_title.strip().replace(" ", "_")

    project_dir = Path("output") / safe_title

    project_dir.mkdir(parents=True, exist_ok=True)

    return project_dir


def save_scene_plan(project_dir, scene_plan):
    """
    Saves the AI-generated scene plan as scenes.json.
    """

    file_path = project_dir / "scenes.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            scene_plan,
            file,
            indent=4,
            ensure_ascii=False
        )

    return file_path