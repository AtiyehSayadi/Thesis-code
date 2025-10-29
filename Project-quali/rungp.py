from main_gp import main
from convert import display_matrix_values, create_matrix_interface

def run_main_with_ui():
    create_matrix_interface()  # This allows the user to create the matrix

    # Get the matrix from the UI
    print("Creating matrix...")
    created_matrix = display_matrix_values()  # Returns the matrix
    print("Matrix created:", created_matrix)

    # Run the main function with the created matrix
    print("Running the main function...")
    best_min, number_generations, best_matrix = main(created_matrix)
    print("Results from main function:")
    print(f"Best Minimum: {best_min}")
    print(f"Number of Generations: {number_generations}")
    print(f"Best Matrix{best_matrix}")


run_main_with_ui()
