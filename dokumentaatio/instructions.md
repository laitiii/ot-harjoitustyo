# Instructions

## Setup

Download the newest source code from the [releases](https://github.com/laitiii/ot-harjoitustyo/releases) by selecting ***Source code*** under ***Assets***

Extract the zip folder. After navigating to the extracted folder in the terminal, run

```bash
poetry install
```

After this, you can start the game with 

```bash
poetry run invoke start
```

## Game 

After starting the game, you will be greeted by the menu screen. From here, you can start the game by pressing space.

### Build phase
The game starts off in the build phase. Here you can prepare for the next wave by building turrets using your money. Turrets are built with the **left mouse button**. 
You can start the next wave of enemies by pressing space. 

### Defense phase
Your turrets will attack enemies automatically. They have an invisible range of 2,5 tiles.

In the defense phase, a wave of enemies will move along the path toward the exit. You must defeat them before they reach the exit.
The enemies will progressively get tougher and grow in number. Try not to get overwhelmed.

After a successful defense phase, you will enter the build phase again. This loops until you run out of lives.

### Game over
If your lives reach zero, you will lose the game and enter the game over screen. From here, you can restart the game by pressing space.

### Controls
- Space = start game/next wave
- Left mouse button = build turret
