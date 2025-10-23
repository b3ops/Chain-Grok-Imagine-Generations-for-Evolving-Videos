# Chain-Grok-Imagine-Generations-for-Evolving-Videos
# Grok Video Chainer

A simple Python tool to chain short video generations from Grok Imagine (xAI's AI video tool). Start with an MP4, extract its last frame, generate a 6-sec evolution clip, repeat, then stitch into one long seamless video.

![Demo Workflow](https://via.placeholder.com/800x400?text=Extract+Generate+Chain+Stitch) <!-- Add a GIF/screenshot here if you make one -->

## Why?
- Grok Imagine (Oct 2025) turns images into 6-sec MP4s with animation/sound.
- This chains them: Original vid → Clip 1 (from last frame) → Clip 2 (from Clip 1's last frame) → etc.
- Perfect for evolving scenes without manual editing.

## Quick Start

1. **Install FFmpeg** (for frame extraction & stitching):
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

2. **Clone & Run**:

   git clone https://github.com/b3oPs/grok-video-chainer.git
   cd grok-video-chainer
   python video_chainer.py --input_video your_start.mp4 --num_iterations 3 --base_prompt "cyberpunk streets" --output_video epic_chain.mp4


3. **During Run** (the magic part):
- Script extracts frame → Pauses with upload instructions.
- Head to [Grok on x.com](https://x.com/grok) or the app (needs Premium+).
- Upload frame, prompt (e.g., "Animate this into 6-sec video of cyberpunk streets awakening"), download MP4.
- Hit Enter in terminal → Repeats for next chain link.
- Auto-stitches at end.

## Args
- `--input_video`: Your starting MP4.
- `--num_iterations`: How many 6-sec clips to chain (default: 3 → ~18 sec total).
- `--base_prompt`: Idea for prompts (e.g., "forest at dusk"—tweak live in Grok).
- `--output_video`: Final MP4 name.
- `--include_original`: Prepend original vid to chain.

## Tips
- Keep prompts consistent for smooth evolution (e.g., add "with rain" each time).
- Clips save to `./clips/`—review before stitching.
- For longer chains, run in batches to avoid fatigue.
- xAI API? Not yet for video—check [x.ai/api](https://x.ai/api) for updates.

## License
MIT—fork, star, share your chains!

Built with ❤️ by Grok (xAI). Questions? Ping @grok on X.
3. 
