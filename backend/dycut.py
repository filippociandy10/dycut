def find_one_optimize(paper_width, paper_height, piece_width, piece_height):
    best_combinations = []
    max_pieces = 0
    
    # Case 1: Fill landscape rows from left to right and replace with portrait rows
    for num_rows in range(1, paper_height // piece_height + 1):
        pieces_in_landscape = (paper_width // piece_width) * num_rows
        remaining_height = paper_height - (num_rows * piece_height)
        
        # Try replacing some landscape rows with portrait rows in the leftover space
        for rows_to_remove in range(0, num_rows + 1):  # Try removing up to all rows
            landscape_pieces = (paper_width // piece_width) * (num_rows - rows_to_remove)
            remaining_height = paper_height - ((num_rows - rows_to_remove) * piece_height)

            # Check if the remaining height can fit portrait pieces
            pieces_in_portrait = (remaining_height // piece_width) * (paper_width // piece_height)

            # Calculate total pieces for this combination
            total_pieces = landscape_pieces + pieces_in_portrait
            if total_pieces >= max_pieces:
                max_pieces = total_pieces
                best_combinations.append({
                    'num_rows_landscape': num_rows - rows_to_remove,
                    'pieces_landscape': landscape_pieces,
                    'pieces_portrait': pieces_in_portrait,
                    'total_pieces': total_pieces,
                    'remaining_height': remaining_height,
                    'rows_removed': rows_to_remove,
                    'case': 'rows'  # Case 1: Rows from left to right
                })
    
    # Case 2: Fill landscape columns from top to bottom and replace with portrait columns
    for num_cols in range(1, paper_width // piece_width + 1):
        pieces_in_landscape = (paper_height // piece_height) * num_cols
        remaining_width = paper_width - (num_cols * piece_width)

        # Try replacing some landscape columns with portrait columns in the leftover space
        for cols_to_remove in range(0, num_cols + 1):  # Try removing up to all columns
            landscape_pieces = (paper_height // piece_height) * (num_cols - cols_to_remove)
            remaining_width = paper_width - ((num_cols - cols_to_remove) * piece_width)

            # Check if the remaining width can fit portrait pieces
            pieces_in_portrait = (remaining_width // piece_height) * (paper_height // piece_width)

            # Calculate total pieces for this combination
            total_pieces = landscape_pieces + pieces_in_portrait
            if total_pieces >= max_pieces:
                max_pieces = total_pieces
                best_combinations.append({
                    'num_cols_landscape': num_cols - cols_to_remove,
                    'pieces_landscape': landscape_pieces,
                    'pieces_portrait': pieces_in_portrait,
                    'total_pieces': total_pieces,
                    'remaining_width': remaining_width,
                    'cols_removed': cols_to_remove,
                    'case': 'columns'  # Case 2: Columns from top to bottom
                })
    
    # Sort the best combinations by total pieces
    best_combinations.sort(key=lambda x: x['total_pieces'], reverse=True)
    return best_combinations, max_pieces

def find_all_optimize(piece_width, piece_height, paper_sizes):
    min_waste = float('inf')
    all_max_pieces = float('-inf')
    for paper in paper_sizes:
        best_combinations, one_max_piece = find_one_optimize(paper.paper_width,paper.paper_height,piece_width,piece_height)
        waste = calculate_waste(paper.paper_width,paper.paper_height,piece_width,piece_height,best_combinations[0]["total_pieces"])
        if waste < min_waste:
            min_waste = waste
            all_max_pieces = one_max_piece
            paper_width = paper.paper_width
            paper_height = paper.paper_height
            best_combi = best_combinations
    min_waste_percentage = round(((min_waste * 100)/(paper_height * paper_width)),2)
    return all_max_pieces, min_waste_percentage, paper_width, paper_height, best_combi[0]
    

def calculate_waste(paper_width, paper_height, piece_width, piece_height, total_pieces):
    # Total area of the paper
    paper_area = paper_width * paper_height
    
    # Area of a single piece
    piece_area = piece_width * piece_height
    
    # Total area covered by the pieces
    pieces_area = total_pieces * piece_area
    
    # Calculate waste
    waste = paper_area - pieces_area
    return waste

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_layout(layout, paper_width, paper_height, piece_width, piece_height):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(1)
    
    ax.set_xlim(0, paper_width)
    ax.set_ylim(0, paper_height)

    # Step 1: Fill the whole paper with a "empty space" color
    rect = patches.Rectangle((0, 0), paper_width, paper_height, linewidth=1, edgecolor='black', facecolor='#e0e0e0')  # Light gray
    ax.add_patch(rect)

    # Step 2: Plot each piece as a filled rectangle with a specific color
    for x, y, w, h in layout:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='#4CAF50')  # Green for pieces
        ax.add_patch(rect)
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()  # Flip the y-axis to align with the usual top-down view of paper
    plt.show()


def visualize_optimized_combination(paper_width, paper_height, piece_width, piece_height, combination):
    layout = []
    
    if combination['case'] == 'rows':
        num_rows_landscape = combination['num_rows_landscape']

        # Fill landscape rows from left to right
        for row in range(num_rows_landscape):
            for col in range(paper_width // piece_width):
                layout.append((col * piece_width, row * piece_height, piece_width, piece_height))

        remaining_height = combination['remaining_height']
        # Fill portrait rows in the remaining space
        for row in range(remaining_height // piece_width):
            for col in range(paper_width // piece_height):
                layout.append((col * piece_height, paper_height - remaining_height + row * piece_width, piece_height, piece_width))

    elif combination['case'] == 'columns':
        num_cols_landscape = combination['num_cols_landscape']

        # Fill landscape columns from top to bottom
        for col in range(num_cols_landscape):
            for row in range(paper_height // piece_height):
                layout.append((col * piece_width, row * piece_height, piece_width, piece_height))

        remaining_width = combination['remaining_width']
        # Fill portrait columns in the remaining space
        for col in range(remaining_width // piece_height):
            for row in range(paper_height // piece_width):
                layout.append((paper_width - remaining_width + col * piece_height, row * piece_width, piece_height, piece_width))

    # Visualize layout with empty space
    visualize_layout(layout, paper_width, paper_height, piece_width, piece_height)


# Example usage
if __name__ == "__main__":
    paper_width = 61  # Width of the paper
    paper_height = 88  # Height of the paper
    piece_width = 33  # Width of the piece
    piece_height = 22  # Height of the piece
    
    # Find the best combinations of rows and columns that maximize cuts
    best_combinations, max_pieces = find_one_optimize(paper_width, paper_height, piece_width, piece_height)
    best_combinations.sort(key=lambda x: x['total_pieces'], reverse=True)
    # Print the best combinations and their results
    print(f"Max pieces: {max_pieces}")
    for combination in best_combinations:
        print(combination)
    waste = calculate_waste(paper_width,paper_height,piece_width,piece_height,best_combinations[0]["total_pieces"])
    print("Waste:", waste)
    print("Waste percentage:", (waste * 100)/(paper_height * paper_width))
    # Visualize one of the best combinations
    visualize_optimized_combination(paper_width, paper_height, piece_width, piece_height, best_combinations[0])
