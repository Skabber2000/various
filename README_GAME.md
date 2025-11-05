# Knights vs Assassins - Strategic Battle Game

A turn-based 2D strategic battle game featuring Knights vs Assassins with different unit types.

## Game Features

### Unit Types

**Knights Team:**
- **Knight Swordsman (Infantry)** 🛡️
  - Health: 100, Attack: 20, Defense: 8
  - Move Range: 2, Attack Range: 1

- **Knight Rider (Cavalry)** 🐴
  - Health: 80, Attack: 25, Defense: 5
  - Move Range: 4, Attack Range: 1

- **Paladin (Special)** 👑
  - Health: 120, Attack: 30, Defense: 10
  - Move Range: 2, Attack Range: 2

**Assassins Team:**
- **Shadow Blade (Infantry)** 🗡️
  - Health: 90, Attack: 25, Defense: 5
  - Move Range: 3, Attack Range: 1

- **Dark Rider (Cavalry)** 🏇
  - Health: 75, Attack: 30, Defense: 4
  - Move Range: 4, Attack Range: 1

- **Master Assassin (Special)** 🦹
  - Health: 100, Attack: 35, Defense: 6
  - Move Range: 3, Attack Range: 2

## How to Play

1. **Select a Unit**: Click on one of your units (Knights - Gold colored)
2. **Move**: Click on an empty cell within the unit's move range (highlighted in green)
3. **Attack**: Click on an enemy unit within attack range (highlighted in red)
4. **End Turn**: Click "End Turn" button when you're done with your moves
5. **AI Turn**: The Assassins (computer) will automatically take their turn

## Game Mechanics

- **Turn-Based**: Knights (human player) goes first, then Assassins (AI)
- **Unit Actions**: Each unit can move once and attack once per turn
- **Damage Calculation**: Damage = Attacker's Attack - Defender's Defense (minimum 1)
- **Victory Condition**: Eliminate all enemy units to win
- **Movement**: Manhattan distance-based movement (no diagonal)
- **Attack Range**: Units can attack within their specified range

## Strategy Tips

1. **Use Cavalry**: High movement range allows flanking maneuvers
2. **Protect Special Units**: They have powerful abilities and longer attack ranges
3. **Infantry Front Line**: Use infantry as a defensive barrier
4. **Range Advantage**: Special units can attack from 2 tiles away
5. **Combined Arms**: Coordinate different unit types for maximum effectiveness

## Technical Details

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Game Logic**: Python classes for units, board, and game state
- **AI**: Simple tactical AI that moves toward and attacks nearest enemies

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Open browser to http://localhost:5000
```

## API Endpoints

- `GET /` - Game interface
- `POST /api/game/new` - Create new game
- `GET /api/game/state` - Get current game state
- `POST /api/game/move` - Move a unit
- `POST /api/game/attack` - Attack with a unit
- `POST /api/game/end-turn` - End current turn
- `POST /api/game/ai-turn` - AI takes turn

## Game Board

- **Size**: 10x8 grid
- **Starting Positions**:
  - Knights start at the bottom (rows 6-7)
  - Assassins start at the top (rows 0-1)
