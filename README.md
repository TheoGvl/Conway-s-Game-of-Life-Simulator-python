# Conway's Game of Life Simulator

A desktop application visualizing John Conway's famous cellular automaton, built natively in Python using the Flet framework. 

## Academic Context
This project serves as a practical demonstration of several core computer science fundamentals:
* **Discrete Mathematics & Automata:** Implementing strict procedural rules (Underpopulation, Survival, Overpopulation, Reproduction) to govern a grid-based ecosystem.
* **Matrix Manipulation:** Separating the application's visual state from the logical state a 2D integer array. 
* **State Management:** Calculating simultaneous generations. The algorithm computes the next generation on a secondary matrix to prevent data corruption that occurs when modifying an array while concurrently iterating over it.

## Features
* **Interactive Canvas:** Click and drag to draw your own custom cellular structures before starting the simulation.
* **Random Seeding:** Instantly populate the board with a randomized ecosystem to watch chaotic systems stabilize into oscillators or still-lifes.
* **Asynchronous Game Loop:** Uses Python's `asyncio` to run the mathematical logic loop without freezing or stuttering the graphical user interface.

## The 4 Rules of Life
Every cell interacts with its eight neighbors horizontally, vertically, and diagonally. At each step in time, the following transitions occur completely simultaneously:
1. Any live cell with fewer than two live neighbors dies.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies.
4. Any dead cell with exactly three live neighbors becomes a live cell.

## Tech Stack & Requirements
* **Language:** Python 3.8+
* **Framework:** 

## How to Run Locally
1. Install the required dependency:
   ```bash
   pip install flet
