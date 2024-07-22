from .utils import find_target_block, parse_LIST_line

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

    for line in block_lines[3:]:
        line_energies, line_cross_sections = parse_LIST_line(line)
        energies.extend(line_energies)
        cross_sections.extend(line_cross_sections)

    return energies, cross_sections
