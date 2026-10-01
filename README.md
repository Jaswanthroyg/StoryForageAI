# StoryForge AI 🎬

StoryForge AI is a Python-based CLI application that transforms a user-provided story into a short AI-generated video.

The application automatically:

1. Analyzes the story using Gemini AI.
2. Creates a structured scene plan.
3. Generates an image for each scene using Pixazo.
4. Generates narration for each scene using Edge TTS.
5. Converts each image + narration into a video scene using FFmpeg.
6. Merges all scene videos.
7. Adds background music.
8. Produces a final outcome as story to MP4 video.

---

## How It Works

```text
User Story
    ↓
Gemini Story Generator
    ↓
Scene Plan (JSON)
    ↓
Pixazo Image Generation
    ↓
Scene Images
    ↓
Edge TTS
    ↓
Narration Audio
    ↓
FFmpeg
    ↓
Individual Scene Videos
    ↓
Video Merger
    ↓
background_music.mp3
    ↓
Final story to MP4 Video

Features

-Story-to-video generation
-AI-powered story analysis
-Automatic scene planning
-AI-generated scene images
-AI-generated narration
-Automatic scene video creation
-Background music integration
-Configurable target video duration
-Retry handling for story generation
-Stage-level error handling
-Automatic project folder creation
-CLI-based workflow

Tech Stack

Technology		Purpose
----------------------------------------------
Python 3.11.9		Application development
Gemini API		Story and scene generation
Pixazo 			Scene image generation
Edge TTS		Narration generation
FFmpeg			Video processing and merging
Requests		HTTP API requests
python-dotenv		Environment variable management

Project Structure

StoryForgeAI/
│
├── ai/
│   ├── story.py
│   ├── image.py
│   └── audio.py
│
├── video/
│   ├── __init__.py
│   ├── composer.py
│   └── merge.py
│
├── utils/
│   ├── files.py
│   └── retry.py
│
├── music/
│   └── Add your own music/background.mp
│
├── output/
│   └── generated projects
│
├── main.py
├── pipeline.py
├── requirements.txt
├── .env
└── .gitignore

Requirements:

Before running StoryForge AI, install:
Python 3.11.9
FFmpeg
Gemini API key
Pixazo API key
FFmpeg must be available through the system PATH.
Verify FFmpeg installation:
ffmpeg -version

Installation

1.Clone the repository:
 git clone <YOUR_GITHUB_REPOSITORY_URL>

2.Enter the project directory:
 cd StoryForgeAI

3.Create a virtual environment:
 python -m venv venv

4.Activate the virtual environment on Windows:
 .\venv\Scripts\Activate.ps1

5.Install Python dependencies:
 pip install -r requirements.txt

Run StoryForge AI

-->Activate the virtual environment:
   .\venv\Scripts\Activate.ps1

-->Run:
   python main.py
   Enter your story when prompted:
   Enter your story:
   > A young farmer discovers a mysterious village hidden in the mountains.
   
StoryForge AI will then execute the complete pipeline automatically

Output

Each generated story creates a project inside:
output/
A generated project contains:

Project_Name/
│
├── scenes.json
├── images/
│   ├── scene_01.png
│   ├── scene_02.png
│   └── ...
│
├── audio/
│   ├── scene_01.mp3
│   ├── scene_02.mp3
│   └── ...
│
├── videos/
│   ├── scene_01.mp4
│   ├── scene_02.mp4
│   └── ...
│
└── Project_Name_final.mp4

Screenshots — for quick understanding

Screenshot 1 — Pipeline running      :docs\Screenshots\pipeline_start.png
Screenshot 2 — image generaton       :docs\Screenshots\image_generation.png
Screenshot 3 — final video generaton :docs\Screenshots\Final_video_generation.png
Screenshot 4 — generated image       :docs\Screenshots\Generated_image.png
Screenshot 5 — Generated video       :docs\Screenshots\generated_video.png

Error Handling

StoryForge AI handles failures at different stages of the pipeline.

Examples include:
-invalid or missing API configuration
-story generation failure
-image generation failure
-narration generation failure
-scene video creation failure
-final video creation failure

The Gemini story-generation stage also uses limited retry attempts with increasing delays.

Future Improvements

Potential future improvements include:
-subtitles/captions
-cinematic transitions and effects
-improved audio mixing
-multiple voice options
-parallel image/audio generation
-additional image-generation providers
-additional TTS providers
-YouTube upload automation
-improved CLI progress reporting
-web interface

Project Status

Current status: Working end-to-end prototype

The complete pipeline has been integrated and tested:

Story
 ↓
Scene Plan
 ↓
Images
 ↓
Narration
 ↓
Scene Videos
 ↓
Final Video

---
## Author

**Jaswanth Roy Gorre**

Python Backend Developer | AI/ML Enthusiast

This project was designed and developed by **Jaswanth Roy**.

- GitHub:   https://github.com/jaswanthroyg
- LinkedIn: https://www.linkedin.com/in/jaswanthroyg?

---

⭐ If you found this project interesting, consider giving the repository a star!






