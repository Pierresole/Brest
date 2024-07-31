from .utils import find_target_block, parse_TAB1

def read_MF3(file_path, targetMT):
    """
    Reads the MF3 section from the given file and target MT, extracting energies and cross-sections.
    
    Parameters:
        file_path (str): Path to the file to be parsed.
        targetMT (int): The target MT number.
    
    Returns:
        energies (list): List of energy values.
        cross_sections (list): List of cross-section values.
    """
    targetMF = 3
    block_lines = find_target_block(file_path, targetMF, targetMT)
    energies = []
    cross_sections = []
    
    C1, C2, L1, L2, NR, NP, NBT, INT, x_values, y_values, new_index =  parse_TAB1(block_lines, 1)

    return x_values, y_values
