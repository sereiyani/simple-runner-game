# Simple Runner Game

A simple endless runner built from scratch with **Python + Pygame** and a pure **browser version** (no install).

Jump over obstacles, rack up points, beat your high score!

## Features

- Smooth jumping physics + gravity
- Randomly sized obstacles
- Score + persistent high score
- Procedural sound effects (jump / score / crash)
- Game Over + instant restart
- Increasing difficulty (browser version)
- GitHub Actions CI that verifies the Python code

## Quick Start (Python)

```bash
git clone https://github.com/sereiyani/simple-runner-game.git
cd simple-runner-game
pip install -r requirements.txt
python runner.py
```

Or:

```bash
make install
make run
# or
./run.sh
```

**Controls**

| Key | Action |
|-----|--------|
| `SPACE` or `↑` | Jump / Restart after Game Over |
| `ESC` | Quit |

High score is saved to `highscore.txt` in the same folder.

## Browser Version (zero install)

Open the file directly or host it:

```bash
# just open in any browser
open web/index.html          # macOS
start web/index.html        # Windows
xdg-open web/index.html     # Linux
```

Or enable **GitHub Pages**:
1. Go to the repository **Settings → Pages**
2. Source: Deploy from a branch → `main` → `/docs` or root (you can move `web/index.html` to root if you prefer)
3. After a minute the game will be live at `https://sereiyani.github.io/simple-runner-game/`

The browser version uses the Web Audio API for beeps and `localStorage` for the high score. Works on desktop and mobile (tap to jump).

## Project Structure

```
simple-runner-game/
├── runner.py              # Desktop game (Pygame)
├── web/
│   └── index.html         # Browser version (Canvas + JS)
├── requirements.txt
├── run.sh
├── Makefile
├── .github/workflows/ci.yml
└── README.md
```

## CI

Every push/PR runs a small GitHub Actions workflow that:
- Installs dependencies
- Verifies `pygame` imports
- Checks Python syntax

You can also trigger it manually from the **Actions** tab.

## Next Ideas

- Animated pixel-art sprites
- More obstacle types (flying, double)
- Background parallax / day-night cycle
- Online leaderboard

Enjoy!
