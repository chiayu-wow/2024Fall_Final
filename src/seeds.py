import numpy as np


def initialize_grid(rows, cols, water_body_ratio=0.2, fire_location=(25, 25), num_water_bodies=2, bush_ratio=0.3,
                    nums_of_busharea=4):
    # Initialize grid: 0 = empty, 1 = tree
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.15, 0.85])  # 15% empty, 85% plants
    grid[fire_location] = 2  # Fire start location

    # Calculate total water cells and assign water areas
    total_water_cells = int(rows * cols * water_body_ratio)
    water_cells_per_body = total_water_cells // num_water_bodies
    all_water_cells = set()

    for _ in range(num_water_bodies):
        water_center = (np.random.randint(0, rows), np.random.randint(0, cols))
        water_cells = {water_center}

        while len(water_cells) < water_cells_per_body:
            current_cell = list(water_cells)[np.random.randint(0, len(water_cells))]
            neighbors = [
                (current_cell[0] + dx, current_cell[1] + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= current_cell[0] + dx < rows and 0 <= current_cell[1] + dy < cols
                   and (current_cell[0] + dx, current_cell[1] + dy) not in all_water_cells
            ]
            if neighbors:
                new_cell = neighbors[np.random.randint(0, len(neighbors))]
                water_cells.add(new_cell)

        all_water_cells.update(water_cells)

    for i, j in all_water_cells:
        grid[i, j] = 3  # Mark water cells

    # Assign bushes to specific areas
    total_trees = np.sum(grid == 1)
    total_bushes = int(total_trees * bush_ratio)
    bushes_per_area = total_bushes // nums_of_busharea
    all_bush_cells = set()

    for _ in range(nums_of_busharea):
        bush_center = (np.random.randint(0, rows), np.random.randint(0, cols))
        while grid[bush_center] != 1:  # Ensure bush center is a tree
            bush_center = (np.random.randint(0, rows), np.random.randint(0, cols))

        bush_cells = {bush_center}

        while len(bush_cells) < bushes_per_area:
            current_cell = list(bush_cells)[np.random.randint(0, len(bush_cells))]
            neighbors = [
                (current_cell[0] + dx, current_cell[1] + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= current_cell[0] + dx < rows and 0 <= current_cell[1] + dy < cols
                   and (current_cell[0] + dx, current_cell[1] + dy) not in all_bush_cells
                   and grid[current_cell[0] + dx, current_cell[1] + dy] == 1  # Only trees become bushes
            ]
            if neighbors:
                new_cell = neighbors[np.random.randint(0, len(neighbors))]
                bush_cells.add(new_cell)

        all_bush_cells.update(bush_cells)

    for i, j in all_bush_cells:
        grid[i, j] = 5  # Mark bush cells

    # Tree types: assign types to trees and bushes
    tree_types = np.empty_like(grid, dtype=object)
    tree_types[grid == 1] = np.random.choice(["pine", "oak", "willow"], size=np.sum(grid == 1))
    tree_types[grid == 5] = "bush"  # Assign bushes explicitly

    return grid, tree_types
