<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=F70000&center=true&vCenter=true&width=435&lines=Joji+Vibe+Controller;Syncs+Music+to+Tuya+Bulbs;Real-time+Color+Extraction" alt="Typing SVG" />
</div>

<div align="center">
  
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Hardware-Tuya_Smart_Bulb-orange?style=for-the-badge&logo=iot" />
  <img src="https://img.shields.io/badge/API-Last.fm-red?style=for-the-badge&logo=last.fm" />

</div>

---

# 🎵 VibeLight: Music-Reactive IoT Lighting

> *"Why settle for a dim room when you can live inside the album cover?"*

VibeLight is a Python-based IoT controller that syncs your smart room lighting to the music you are currently playing. Unlike simple color grabbers, it uses **K-Means Clustering** and **Custom Saturation Biasing** to ensure the lights capture the *mood* of the song, not just the average pixel.

![Demo of Lights](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3AybnFqY2k.../placeholder.gif)

## 🚀 Features

* **🎨 True-Tone Extraction:** Uses `K-Means` clustering (k=6) to separate dominant colors from background noise.
* **🧠 "Joji Mode" (Red Bias):** Custom algorithm that prioritizes deep, saturated colors (like Dark Red) over washed-out skin tones or grays.
* **💡 Neon Boost:** Automatically detects "muddy" colors and boosts saturation/brightness to maximize LED hardware potential.
* **👁️ Gamma Correction:** Corrects RGB values to match human eye perception vs. LED linear output.
* **🛑 Auto-Shutdown:** Detects when music stops (Last.fm API) and automatically resets lights to Warm White after a timeout.
* **🛡️ Fail-Safe:** Includes `atexit` handlers to reset lights even if the script crashes or is force-killed.

## 🛠️ Tech Stack

* **Core:** Python 3
* **APIs:** Last.fm (scrobbling data), Tuya (hardware control)
* **Libraries:** `requests`, `pillow` (image processing), `scikit-learn` (clustering), `tinytuya`, `webcolors`

## ⚙️ How It Works (The Logic)

1.  **Poll Last.fm:** Checks for the `nowplaying` attribute.
2.  **Fetch Art:** Downloads the high-res album cover.
3.  **Process Image:** * Resizes to 50x50 for speed.
    * Converts to RGB (strips Alpha channels).
4.  **Analyze Color:** * Runs K-Means to find 6 dominant color centers.
    * **Selection Logic:** Scores colors based on saturation. Applies a **1.3x multiplier** bonus to Red/Pink hues to capture "moody" aesthetics.
5.  **Hardware Translation:**
    * Applies Gamma Correction (2.8).
    * Boosts Saturation (1.5x) while capping at 100%.
    * Maps to Tuya's 0-1000 scale (or 0-255) for physical output.

## 📦 Installation

1.  **Clone the repo**
    ```bash
    git clone [https://github.com/yourusername/vibelight.git](https://github.com/yourusername/vibelight.git)
    cd vibelight
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Keys**
    Open `main.py` and replace the placeholder text with your actual API keys:
    * `LASTFM_API_KEY = "YOUR_KEY_HERE"`
    * `TUYA_DEVICE_ID = "YOUR_ID_HERE"`
    * `TUYA_LOCAL_KEY = "YOUR_KEY_HERE"`

4.  **Run it**
    ```bash
    python main.py
    ```

## 📸 Examples

| Album Art | Raw Color | VibeLight Output |
| :---: | :---: | :---: |
| **Ballads 1** (Joji) | `[100, 40, 40]` (Muddy Brown) | `[255, 20, 20]` (Neon Red) |
| **Igor** (Tyler) | `[200, 150, 150]` (Pale Pink) | `[255, 50, 150]` (Hot Pink) |

## 🤝 Contributing

Forks are welcome! I'm currently working on adding Spotify support and local audio analysis.

---
<div align="center">
  Built with ❤️ and Python by Harshil
</div>