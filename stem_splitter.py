#!/usr/bin/env python3
"""
A Python script that uses Demucs to separate audio files into stems.

This script:
- Prompts the user for a folder containing audio files.
- Searches the folder for audio files (e.g. .wav, .mp3, .flac, .ogg, .opus, .m4a).
- Asks the user how they want to split the audio:
    Option 1: Default 4 stems (drums, bass, vocals, other)
    Option 2: 2 stems (typically vocals and accompaniment)
- Calls Demucs with the chosen parameters.
- Outputs the separated stems in the same folder (using Demucs’s --out argument).
"""

import os
import glob
import subprocess
import sys


def get_audio_files(folder):
    """Returns a list of audio files in the given folder."""
    extensions = ('*.wav', '*.mp3', '*.flac', '*.ogg', '*.opus', '*.m4a')
    audio_files = []
    for ext in extensions:
        audio_files.extend(glob.glob(os.path.join(folder, ext)))
    return audio_files


def get_user_choice():
    """Prompts the user to select an audio separation mode."""
    print("\nSplit options:")
    print("1. Default (4 stems: drums, bass, vocals, other)")
    print("2. 2-stems (vocals and accompaniment)")
    choice = input("Enter your choice (1 or 2): ").strip()
    return choice


def build_demucs_command(folder, audio_files, choice):
    """Constructs the Demucs command based on user choice."""
    cmd = ["demucs", "--out", folder]
    if choice == "2":
        cmd.extend(["--two-stems", "vocals"])
    elif choice != "1":
        print("Invalid choice; defaulting to 4-stems separation.")
    cmd.extend(audio_files)
    return cmd


def run_demucs(cmd):
    """Executes the Demucs command."""
    print("\nRunning Demucs with the following command:")
    print(" ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running Demucs:", e)
        sys.exit(1)


def main():
    """Main function to handle user input and execute Demucs."""
    folder = input("Enter the folder path containing audio files: ").strip()
    if not os.path.isdir(folder):
        print("Invalid folder path.")
        sys.exit(1)

    audio_files = get_audio_files(folder)
    if not audio_files:
        print("No audio files found in the folder.")
        sys.exit(1)

    choice = get_user_choice()
    cmd = build_demucs_command(folder, audio_files, choice)
    run_demucs(cmd)

    print("\nDemucs processing completed.")
    print("The separated stems have been saved in the folder:", folder)


if __name__ == "__main__":
    main()
