import flet as ft
import asyncio
import random

def main(page: ft.Page):
    page.title = "Conway's Game of Life"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Grid Dimensions Kept slightly smaller for smooth UI performance
    ROWS = 20
    COLS = 30
    CELL_SIZE = 25

    # Colors
    COLOR_DEAD = ft.Colors.BLUE_GREY_900
    COLOR_ALIVE = ft.Colors.CYAN_400

    # State Variables
    is_running = False
    grid_state = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    grid_cells = []

    def handle_click(e):
        """Allows the user to click cells to manually toggle them alive or dead."""
        if is_running:
            return  # Prevent drawing while the simulation is actively calculating

        # Get coordinates from the control's data attribute
        r, c = e.control.data 
        
        # Toggle state
        if grid_state[r][c] == 0:
            grid_state[r][c] = 1
            e.control.bgcolor = COLOR_ALIVE
        else:
            grid_state[r][c] = 0
            e.control.bgcolor = COLOR_DEAD
            
        page.update()

    def count_neighbors(r, c):
        """Calculates how many living cells surround a specific coordinate."""
        count = 0
        # Check all 8 surrounding cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the center cell itself
                
                nr, nc = r + dr, c + dc
                # Check boundaries so we don't throw an IndexError
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    count += grid_state[nr][nc]
        return count

    async def toggle_simulation(e):
        """Starts or stops the main game loop."""
        nonlocal is_running
        
        if is_running:
            is_running = False
            btn_play.text = "Start Simulation"  # type: ignore
            btn_play.icon = ft.Icons.PLAY_ARROW
            btn_play.color = ft.Colors.GREEN_400
            page.update()
            return

        is_running = True
        btn_play.text = "Pause Simulation"  # type: ignore
        btn_play.icon = ft.Icons.PAUSE
        btn_play.color = ft.Colors.AMBER_400
        page.update()

        # The Game Loop
        while is_running:
            # We must compute the next generation in a separate matrix
            # to prevent altering the board while we are still checking it!
            new_state = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            
            for r in range(ROWS):
                for c in range(COLS):
                    alive_neighbors = count_neighbors(r, c)
                    
                    if grid_state[r][c] == 1:
                        # Rule 1 & 3: Underpopulation or Overpopulation -> Dies
                        # Rule 2: 2 or 3 neighbors -> Lives
                        if alive_neighbors in [2, 3]:
                            new_state[r][c] = 1
                        else:
                            new_state[r][c] = 0
                    else:
                        # Rule 4: Reproduction -> Exactly 3 neighbors spawns a new cell
                        if alive_neighbors == 3:
                            new_state[r][c] = 1

            # Apply the new state to the real grid and update the UI
            for r in range(ROWS):
                for c in range(COLS):
                    grid_state[r][c] = new_state[r][c]
                    color = COLOR_ALIVE if new_state[r][c] == 1 else COLOR_DEAD
                    
                    # Only update the Flet UI if the cell actually changed color (saves performance)
                    if grid_cells[r][c].bgcolor != color:
                        grid_cells[r][c].bgcolor = color
            
            page.update()
            await asyncio.sleep(0.1) # Speed of the simulation

    def clear_board(e):
        """Kills all cells and stops the simulation."""
        nonlocal is_running
        is_running = False
        btn_play.text = "Start Simulation"  # type: ignore
        btn_play.icon = ft.Icons.PLAY_ARROW
        btn_play.color = ft.Colors.GREEN_400

        for r in range(ROWS):
            for c in range(COLS):
                grid_state[r][c] = 0
                grid_cells[r][c].bgcolor = COLOR_DEAD
        page.update()

    def randomize_board(e):
        """Randomly seeds the board with live cells."""
        if is_running:
            return
            
        for r in range(ROWS):
            for c in range(COLS):
                # 25% chance for a cell to spawn alive
                is_alive = 1 if random.random() > 0.75 else 0
                grid_state[r][c] = is_alive
                grid_cells[r][c].bgcolor = COLOR_ALIVE if is_alive else COLOR_DEAD
        page.update()

    # --- UI Components ---
    title = ft.Text("Conway's Game of Life", size=32, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Draw your pattern or click Randomize, then press Start.", color=ft.Colors.GREY_400)

    btn_play = ft.Button("Start Simulation", icon=ft.Icons.PLAY_ARROW, on_click=toggle_simulation, color=ft.Colors.GREEN_400)
    btn_random = ft.Button("Randomize", icon=ft.Icons.SHUFFLE, on_click=randomize_board, color=ft.Colors.BLUE_400)
    btn_clear = ft.Button("Clear Board", icon=ft.Icons.DELETE, on_click=clear_board, color=ft.Colors.RED_400)

    controls_row = ft.Row([btn_play, btn_random, btn_clear], alignment=ft.MainAxisAlignment.CENTER)

    # Generate the Grid UI
    grid_column = ft.Column(spacing=2)
    for r in range(ROWS):
        row_cells = []
        ui_row = ft.Row(spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        for c in range(COLS):
            cell = ft.Container(
                width=CELL_SIZE,
                height=CELL_SIZE,
                bgcolor=COLOR_DEAD,
                border_radius=4,
                data=(r, c), # Store coordinates directly inside the UI object
                on_click=handle_click,
            )
            row_cells.append(cell)
            ui_row.controls.append(cell)
        grid_cells.append(row_cells)
        grid_column.controls.append(ui_row)

    page.add(title, subtitle, controls_row, ft.Container(height=10), grid_column)

ft.run(main)