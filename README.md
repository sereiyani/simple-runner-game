# Simple Runner Game

A simple endless runner game built from scratch with **Python + Pygame**.

Jump over red obstacles, survive as long as you can, and beat your high score!

## Features
- Smooth jumping physics
- Randomly sized obstacles
- Score tracking
- Game Over + instant restart
- Clean, beginner-friendly code

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/sereiyani/simple-runner-game.git
cd simple-runner-game
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Play!
```bash
python runner.py
```

Or use the convenience scripts:

```bash
# Shell script
chmod +x run.sh
./run.sh

# Makefile
make run
```

## Controls
| Key        | Action              |
|------------|---------------------|
| `SPACE` or `↑` | Jump / Restart after Game Over |
| `ESC`      | Quit                |

## Project Structure
```
simple-runner-game/
├── runner.py          # Main game code
├── requirements.txt   # Dependencies
├── run.sh             # One-click run script
├── Makefile           # make run / make install
└── README.md
```

## Next Ideas
- Add sound effects
- Animated sprites
- Increasing difficulty
- High score saving
- Different obstacle types

Enjoy and happy coding!
