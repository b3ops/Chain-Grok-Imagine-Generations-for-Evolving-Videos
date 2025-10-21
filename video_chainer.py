#!/usr/bin/env python3
"""
Video Chainer: Extract last frame from MP4 → Upload to Grok Imagine → Generate 6-sec clip → Repeat for chained evolution → Stitch into long video.

Requirements:
- FFmpeg installed (brew install ffmpeg on macOS; apt install ffmpeg on Linux).
- Python 3.x (stdlib only—no extras needed).
- Grok Premium+ or SuperGrok for Imagine video gen (x.com or app).

Usage:
    python video_chainer.py --input_video start.mp4 --num_iterations 3 --base_prompt "cyberpunk city" --output_video chain.mp4 --include_original

Author: Built with Grok by xAI (Oct 2025).
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def run_ffmpeg(cmd, check=True):
    """Run FFmpeg command and handle errors."""
    try:
        subprocess.run(cmd, check=check, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr}")
        sys.exit(1)

def extract_last_frame(input_video):
    """Extract last frame using FFmpeg."""
    output_img = f"frame_{Path(input_video).stem}.jpg"  # Unique per video
    print(f"Extracting last frame from {input_video}...")
    
    # Count frames
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_frames", "-of", "csv=p=0", input_video
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    total_frames = int(result.stdout.strip())
    
    if total_frames == 0:
        print("Error: No frames in video.")
        sys.exit(1)
    
    # Extract last frame
    extract_cmd = [
        "ffmpeg", "-i", input_video, "-vf", f"select=eq(n\\,{total_frames-1})",
        "-vframes", "1", "-y", output_img
    ]
    run_ffmpeg(extract_cmd)
    print(f"Last frame saved to: {output_img}")
    return output_img

def generate_clip_instructions(current_video, iteration, num_iterations, base_prompt, frame_img, clips_dir):
    """Print instructions for manual Grok Imagine generation."""
    next_clip = clips_dir / f"clip_{iteration:03d}.mp4"
    remaining = num_iterations - iteration + 1
    
    print(f"\n=== ITERATION {iteration}/{num_iterations}: Generate Next Clip ===")
    print(f"Current video: {current_video}")
    print(f"1. Open Grok on x.com or the Grok app (Premium+ or SuperGrok for full access).")
    print(f"2. Upload '{frame_img}' as the starting image.")
    print(f"3. Enter your own prompt, e.g., 'Using this image as the starting frame, generate a 6-second MP4 video (with smooth animation and optional sound) of [your evolving scene description].'")
    print(f"   (Tip: Build on the base idea '{base_prompt}' for continuity, like adding 'with emerging lights' for iteration {iteration}.)")
    print(f"4. Download the generated MP4 and save it as '{next_clip}'.")
    print(f"5. Once saved, press Enter to proceed to next iteration (or extraction if last)...")
    input()
    return next_clip

def stitch_clips(clips_dir, output_video, include_original=False, original_video=None):
    """Stitch all clips using FFmpeg concat."""
    list_file = "video_list.txt"
    clips = sorted(clips_dir.glob("clip_*.mp4"))
    
    if not clips:
        print("No clips to stitch!")
        return
    
    # Create concat list
    with open(list_file, "w") as f:
        if include_original and original_video:
            f.write(f"file '{original_video}'\n")
        for clip in clips:
            f.write(f"file '{clip}'\n")
    
    # Stitch
    print(f"Stitching {len(clips)} clips (plus original if included) into {output_video}...")
    concat_cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file,
        "-c", "copy", "-y", output_video
    ]
    run_ffmpeg(concat_cmd)
    
    # Cleanup
    os.remove(list_file)
    print(f"Final chained video saved to: {output_video}")
    print(f"Total length: ~{len(clips) * 6} seconds (excluding original).")

def main():
    parser = argparse.ArgumentParser(description="Video Chainer: Chain generations via Grok Imagine for longer evolving videos.")
    parser.add_argument("--input_video", required=True, help="Starting MP4 video.")
    parser.add_argument("--num_iterations", type=int, default=3, help="Number of chained generations (default: 3).")
    parser.add_argument("--base_prompt", default="an evolving surreal landscape", help="Base prompt for Grok Imagine (default: 'an evolving surreal landscape').")
    parser.add_argument("--output_video", default="chained_video.mp4", help="Final stitched video path (default: chained_video.mp4).")
    parser.add_argument("--include_original", action="store_true", help="Include the original video at the start of the chain.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_video):
        print(f"Error: {args.input_video} not found.")
        sys.exit(1)
    
    clips_dir = Path("clips")
    clips_dir.mkdir(exist_ok=True)
    
    current_video = args.input_video
    iteration = 1
    
    # Loop for chaining
    while iteration <= args.num_iterations:
        # Extract last frame
        frame_img = extract_last_frame(current_video)
        
        # Manual generation
        next_clip = generate_clip_instructions(
            current_video, iteration, args.num_iterations, args.base_prompt, frame_img, clips_dir
        )
        
        # Verify next clip exists before proceeding
        if not next_clip.exists():
            print(f"Error: {next_clip} not found. Generate it first!")
            sys.exit(1)
        
        current_video = next_clip
        iteration += 1
    
    # Stitch all
    stitch_clips(clips_dir, args.output_video, args.include_original, args.input_video if args.include_original else None)
    
    print("Chain complete! Your evolving video is ready.")

if __name__ == "__main__":
    main()
