def find_one_optimize(paper_width, paper_height, piece_width, piece_height):
    best_combinations = []
    max_pieces = 0
    
    # Try all possible combinations of rows and columns with both orientations
    for num_rows in range(1, paper_height // piece_height + 1):
        # Step 1: Fill the paper with landscape pieces first
        pieces_in_landscape = (paper_width // piece_width) * num_rows
        remaining_height = paper_height - (num_rows * piece_height)
        
        # Step 2: Check if we can replace some landscape rows with portrait rows in the leftover space
        for rows_to_remove in range(0, num_rows + 1):  # Try removing up to all the rows
            landscape_pieces = (paper_width // piece_width) * (num_rows - rows_to_remove)
            remaining_height = paper_height - ((num_rows - rows_to_remove) * piece_height)
            
            # Step 3: Check if the leftover space can fit portrait pieces
            pieces_in_portrait = (remaining_height // piece_width) * (paper_width // piece_height)
            
            # Total pieces after rearranging
            total_pieces = landscape_pieces + pieces_in_portrait
            if total_pieces > max_pieces:
                max_pieces = total_pieces
                best_combinations.append({
                    'num_rows_landscape': num_rows - rows_to_remove,
                    'pieces_landscape': landscape_pieces,
                    'pieces_portrait': pieces_in_portrait,
                    'total_pieces': total_pieces,
                    'remaining_height': remaining_height,
                    'rows_removed': rows_to_remove
                })
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
    return all_max_pieces, min_waste, paper_width, paper_height, best_combi[0]
    

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

def visualize_layout(layout, paper_width, paper_height):
    fig, ax = plt.subplots(1)
    
    # Set the size of the canvas
    ax.set_xlim(0, paper_width)
    ax.set_ylim(0, paper_height)
    
    # Plot each piece as a rectangle
    for x, y, w, h in layout:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()  # Flip the y-axis to align with the usual top-down view of paper
    plt.show()

def visualize_optimized_combination(paper_width, paper_height, piece_width, piece_height, combination):
    layout = []
    num_rows_landscape = combination['num_rows_landscape']
    
    # Fill landscape pieces
    for row in range(num_rows_landscape):
        for col in range(paper_width // piece_width):
            layout.append((col * piece_width, row * piece_height, piece_width, piece_height))
    
    # Fill portrait pieces in the remaining height
    remaining_height = combination['remaining_height']
    for row in range(remaining_height // piece_width):
        for col in range(paper_width // piece_height):
            layout.append((col * piece_height, paper_height - remaining_height + row * piece_width, piece_height, piece_width))
    
    # Visualize layout
    visualize_layout(layout, paper_width, paper_height)


# Example usage
if __name__ == "__main__":
    paper_width = 67  # Width of the paper
    paper_height = 35  # Height of the paper
    
    piece_width = 22  # Width of the piece
    piece_height = 15  # Height of the piece
    
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
