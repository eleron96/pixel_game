
# Pixel Game 🎮

**Pixel Game** is a simple, pixel-based interactive game developed using Python and Pygame.

![Pixel_Game](https://i.imgur.com/Y7KrBpz.gif)

## Features

- **Interactive Gameplay**: Control and interact with pixels on your screen.
- **Customizable Settings**: Adjust various settings like pixel size and physics properties.
- **Physics-based Dynamics**: Experience realistic physical behaviors in-game.

## Installation and Setup

Ensure you have Python installed, then set up the game using Poetry for dependency management.

### Install Poetry

Install Poetry if it's not already installed:

```bash
pip install poetry
```

### Setup and Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/eleron96/pixel_game.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd pixel_game
   ```
3. **Install dependencies** using Poetry:
   ```bash
   poetry install
   ```
4. **Run the game** using the Makefile:
   ```bash
   make run
   ```

Alternatively, you can run the game directly using Poetry:
```bash
poetry run python main.py
```

![Pixel_game_menu](https://i.imgur.com/KJEZ0bI.gif)

## Configuration

Modify game settings by editing configurations in `pixel_game/menu/settings.py`. Core gameplay mechanics can be found and altered in `pixel_game/logic/game_logic.py`.

