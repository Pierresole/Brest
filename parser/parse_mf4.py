from .utils import find_target_block, parse_line, parse_LIST, custom_to_float, parse_TAB2, parse_TAB1


def parse_legendre_coefficients(lines):
    legendre_data = {}
    for line in lines:
        energy = custom_to_float(line[0:11])
        coefficients = [custom_to_float(line[i:i+11]) for i in range(22, len(line), 11)]
        legendre_data[energy] = coefficients
    return legendre_data

def parse_tabulated_data(lines):
    tabulated_data = {}
    for line in lines:
        energy = custom_to_float(line[0:11])
        mu_values = [custom_to_float(line[i:i+11]) for i in range(22, 22 + 11 * (len(line) // 22))]
        f_values = [custom_to_float(line[i:i+11]) for i in range(22 + 11 * (len(line) // 22), len(line), 11)]
        tabulated_data[energy] = (mu_values, f_values)
    return tabulated_data

def read_MF4(file_path, targetMT):
    targetMF = 4
    block_lines = find_target_block(file_path, targetMF, targetMT)
    ltt = parse_line(block_lines[0])[3]
    # Parse metadata from the first line of the block
    
    # Read NE1 from the third line (index 2)
    NE1 = int(parse_line(block_lines[2])[5])
    
    legendre_data = {}
    tabulated_data = {}

    current_index = 3  # Start reading after the first three lines
    
    if ltt == 1:
        for _ in range(NE1):
            energy, coefficients, new_index = parse_LIST(block_lines, current_index)
            legendre_data[energy] = coefficients
            current_index = new_index
    elif ltt == 2:
        NE2, new_index = parse_TAB2(block_lines, current_index)
        current_index = new_index
        for _ in range(NE2):
            energy, values, new_index = parse_TAB1(block_lines, current_index)
            tabulated_data[energy] = values
            current_index = new_index
    elif ltt == 3:
        for _ in range(NE1):
            energy, coefficients, new_index = parse_LIST(block_lines, current_index)
            legendre_data[energy] = coefficients
            current_index = new_index
        NE2, new_index = parse_TAB2(block_lines, current_index)
        current_index = new_index
        for _ in range(NE2):
            C1, C2, L1, L2, NR, NP, NBT, INT, mu_values, f_values, new_index = parse_TAB1(block_lines, current_index)
            tabulated_data[C2] = (mu_values, f_values)
            current_index = new_index
    else:
        raise ValueError("Unsupported LTT value")

    return ltt, legendre_data, tabulated_data


# def read_MF4(file_path, targetMT):
#     targetMF = 4
#     block_lines = find_target_block(file_path, targetMF, targetMT)
    
#     ltt = parse_line(block_lines[0])[3]
#     # Parse metadata from the first line of the block
    
#     # Read NE1 from the third line (index 2)
#     NE1 = int(parse_line(block_lines[2])[5])
    
#     legendre_data = {}
#     tabulated_data = {}

#     current_index = 4  # Start reading after the first three lines

#     if ltt == 1:
#         for _ in range(NE1):
#             energy, coefficients, new_index = parse_LIST(block_lines, current_index)
#             legendre_data[energy] = coefficients
#             current_index = new_index
#     elif ltt == 2:
#         for _ in range(NE1):
#             energy, tabulated_values, new_index = parse_LIST(block_lines, current_index)
#             tabulated_data[energy] = tabulated_values
#             current_index = new_index
#     elif ltt == 3:
#         for _ in range(NE1):
#             energy, coefficients, new_index = parse_LIST(block_lines, current_index)
#             legendre_data[energy] = coefficients
#             current_index = new_index
#         for _ in range(NE1):
#             energy, tabulated_values, new_index = parse_LIST(block_lines, current_index)
#             tabulated_data[energy] = tabulated_values
#             current_index = new_index
#     else:
#         raise ValueError("Unsupported LTT value")

#     return ltt, legendre_data, tabulated_data

