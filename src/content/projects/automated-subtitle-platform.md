---
title: "Automated Subtitle Generation Platform"
description: "An end-to-end pipeline for generating, formatting, and refining subtitles from video/audio files using OpenAI's Whisper model."
date: 2024-10-05
categories: ["AI", "Automation"]
tags: ["Python", "Whisper", "Cloud Storage", "Web UI"]
technologies: ["Python", "Whisper", "Cloud Storage", "Web UI"]
status: "Completed"
---

# Automated Subtitle Generation Platform

## Overview

Creating accurate subtitles is a time-consuming and often expensive process, especially for high volumes of video content. I developed an automated platform that leverages state-of-the-art speech-to-text models to generate, format, and refine subtitles from raw audio or video files.

The goal was to build a seamless pipeline that takes a raw media file as input and produces production-ready `.srt` or `.vtt` files, minimizing the manual effort required for transcription and synchronization.

## Architecture

The platform is designed as an asynchronous, worker-based system to handle the heavy computational load of audio processing and speech-to-text inference.

### 1. The Ingestion Pipeline
The process begins when a user uploads a media file through a React-based Web UI.
*   **Storage:** The raw file is immediately uploaded to **Google Cloud Storage**, which serves as our primary data lake.
*   **Trigger:** The upload event triggers a Cloud Pub/Sub message, which notifies our orchestration service.

### 2. The Processing Engine (The Core)
The core logic resides in a set of specialized workers running on GPU-enabled instances (or Cloud Run with high-performance configurations).

*   **Audio Extraction:** Using `ffmpeg`, we first extract the high-quality audio stream from the video container to reduce the data volume for the transcription stage.
*   **Transcription with Whisper:** We utilize OpenAI's [Whisper](https://github.com/openai/whisper) model. Whisper is exceptionally robust to different accents, background noise, and technical terminology. We use the `large-v3` model for maximum accuracy, running it on local GPU hardware to keep costs low and performance high.
*   **Timestamping & Segmentation:** Whisper provides word-level timestamps, which are critical for subtitle synchronization. We use these to segment text into "subtitle blocks" that adhere to standard reading speeds and character-per-line limits.

### 3. The Refinement Workflow
Transcription is rarely perfect. The platform provides two ways to refine the output:
*   **Automated LLM Refinement:** A secondary pass using an LLM (like GPT-4o) to correct common transcription errors, improve punctuation, and ensure the text flows naturally within the subtitle constraints.
*   **Manual Editor Interface:** A web-based editor that allows users to view the video alongside the generated subtitles, enabling easy manual adjustments to text and timing.

## Technical Challenges

### 1. Managing Long-Form Audio
Processing a two-hour podcast is vastly different from processing a 30-second clip. Large files can lead to memory exhaustion and timeout issues.

**Solution:** I implemented a **sliding-window chunking strategy**. Instead of feeding a massive audio file to the model at once, we split the audio into overlapping segments. This ensures the model maintains context across the boundaries while keeping the memory footprint manageable.

### 2. Subtitle Timing and Readability
A common problem with automated subtitles is "text jitter" or blocks that are too long to read before they disappear.

**Solution:** I developed a custom **Subtitle Layout Engine**. This engine calculates the number of characters per second (CPS) and characters per line (CPL). If a segment exceeds these limits, the engine automatically triggers a "smart split," finding a natural linguistic break (like a comma or a period) to divide the subtitle into two parts.

### 3. Handling Background Noise and Overlapping Speech
In real-world scenarios, background music or multiple people talking over each other can cause transcription failure.

**Solution:** We integrated a pre-processing step using **source separation** technologies (like Spleeter) to isolate the primary vocal track from background music or noise before passing it to Whisper. This significantly improved word error rates (WER) in "noisy" environments.

## Lessons Learned

*   **Hardware is the Bottleneck:** For speech-to-text, the quality of the user experience is directly tied to GPU availability. Moving from CPU-based inference to GPU-accelerated inference reduced processing time by a factor of 10x.
*   **The "Last Mile" is Human:** Machine transcription gets you 95% of the way there, but the final 5% (the nuance, the specific brand names, the perfect timing) still requires human oversight. The platform's value lies in making that 5% as easy as possible.
*   **Format Versatility:** Providing multiple output formats (`.srt`, `.vtt`, `.ass`) is essential for compatibility with different video players and professional editing suites.

## Conclusion

The Automated Subtitle Generation Platform demonstrates how combining powerful pre-trained models like Whisper with intelligent segmentation and refinement workflows can transform a manual, painstaking task into a high-speed, scalable automated service.
