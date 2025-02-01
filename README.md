## Overview

The SET game is grounded in mathematical and cognitive principles, particularly involving pattern recognition, set theory, and quick decision-making. Each card in SET displays four features: number (1, 2, or 3), color (red, green, or yellow), shading (solid, striped, or open), and shape (ovals, squiggles, diamonds). Players must identify sets of three cards where each attribute is all the same or all different.
The mathematical foundation of SET stems from combinatorics and pattern recognition, and its core challenge is how to efficiently identify valid sets while providing real-time interactive feedback, which is our main goal in realizing the SET game.

## Why This Code?

The purpose of this implementation is to offer an educational tool for individuals interested in understanding the mechanics of the SET card game through coding. It is designed for those with a basic background in Python and can be an excellent project for aspiring game developers or programmers.

## Prerequisites

Before you install and run the game, make sure you have the following:

- **Python**: Version 3.x [Download Python](https://www.python.org/downloads/)
- **Pygame**: This can be installed using pip, which comes with Python. To install Pygame, open your command line and enter:```pip install pygame```

## Installation

To set up the SET game on your local system, follow these steps: Clone the Repository:
git clone [https://github.com/Ruohann/SET](https://github.com/chuuu339/SET-Chu-Tongxin/edit/main/README.md) cd SET
```git clone [https://github.com/Ruohann/SET]cd SET```

## Game Interface

**Card Display Area**

Grid Layout: The game displays cards in a 3x4 grid. Each card represents a unique combination of attributes such as number, symbol, color, and shading.

**Card Selection**

Players can select a card by clicking on it. Selected cards are highlighted with a border around them. If three cards are selected, the game checks if they form a valid set

**Dynamic Updates**

As sets are found and removed from the display, new cards are dealt from the deck to replace them, ensuring the grid is always full until the deck is depleted.

**Score Tracking** 

The player's score is displayed at the top left corner of the window. The score increases by a set amount each time a valid set is successfully identified.

**Timer**

There is a countdown timer displayed at the top right corner of the window. The duration of the timer can be set at the beginning of the game based on the selected difficulty level. The game ends when the timer runs out.


