# Sisak Adventure

## Overview
This project is a card-based roguelike game inspired by "Slay the Spire". Players will navigate through various screens to select characters, edit their decks, and engage in gameplay.

## Project Structure
```
my-pygame-game
├── src
│   ├── main.py                # Entry point of the game
│   ├── screens                # Contains different game screens
│   │   ├── start_screen.py    # Start screen functionality
│   │   ├── choose_player_screen.py # Character selection screen
│   │   ├── tavern_screen.py    # Tavern for editing cards
│   │   └── gameplay_screen.py   # Main gameplay loop
│   ├── assets                  # Game assets
│   │   ├── images              # Image files (backgrounds, sprites, etc.)
│   │   └── sounds              # Sound files (music, effects)
│   └── utils                  # Utility functions
│       └── helpers.py         # Helper functions for various tasks
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/my-pygame-game.git
   ```
2. Navigate to the project directory:
   ```
   cd my-pygame-game
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Gameplay Mechanics
- **Start Screen**: Players can start the game and navigate to the character selection screen.
- **Choose Player Screen**: Players select their character from a list of available options.
- **Tavern Screen**: Players can edit their selected cards and manage their deck.
- **Gameplay Screen**: The main game loop where players encounter enemies and progress through the game.

## Contributing
Feel free to submit issues or pull requests if you would like to contribute to the project. 

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
