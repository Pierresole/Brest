import pickle
import re
import numpy as np

def parse_ID_line(line):
    # Extract the last 14 digits of the line (excluding spaces)
    pos = line.strip()[66:]

    # Digits 0,1,2 and 3 of POS make a number called MAT
    mat = int(pos[0:4])

    # Digits 4 and 5 of POS make a number called MF
    mf = int(pos[4:6])

    # Digits 6, 7 and 8 of POS make a number called MT
    mt = int(pos[6:9])

    return mat, mf, mt

def parse_line(line):
    """
    Parse a single line into a list of floats.
    
    Parameters:
        line (str): The line to parse.
        
    Returns:
        list of float: The parsed values.
    """
    # Extract the first 66 characters of the line
    data_section = line[:66]

    # Split the data into blocks of 11 characters
    blocks = re.findall(r'.{11}', data_section)

    # Convert each block to float using custom notation
    values = [custom_to_float(block) for block in blocks if block.strip()]

    return values

def custom_to_float(s):
    """
    Convert a custom string representation of a float into a float.
    
    Parameters:
        s (str): The string to convert.
        
    Returns:
        float: The converted float.
    """
    s = s.strip().replace(' ', '')
    
    if len(s) == 0:
        return float('nan')  # or return None if that makes more sense in your context

    # Regular expression to match the base and exponent parts
    match = re.match(r'^([+-]?\d*\.?\d*)([eE]?[+-]?\d+)?$', s)
    
    if match:
        base_part = match.group(1)
        exponent_part = match.group(2)

        base = float(base_part) if base_part else 0.0
        if exponent_part:
            exponent = int(exponent_part)  # Convert the exponent part directly
            return base * (10 ** exponent)
        else:
            return base
    else:
        # Handle cases where the string might end with an exponent without 'e' or 'E'
        if len(s) > 2 and s[-2] in ['+', '-'] and s[:-2].replace('.', '').isdigit():
            base = float(s[:-2])
            exponent = int(s[-2:])
            return base * (10 ** exponent)
        return float(s)

def parse_TAB1(lines, start_idx):
    header_values = parse_line(lines[start_idx])
    C1 = header_values[0]
    C2 = header_values[1]
    L1 = header_values[2]
    L2 = header_values[3]
    NR = int(header_values[4])
    NP = int(header_values[5])

    NBT = []
    INT = []

    # Parse NBT and INT values from the second line
    second_line_values = parse_line(lines[start_idx + 1])
    for i in range(NR):
        NBT.append(int(second_line_values[2 * i]))
        INT.append(int(second_line_values[2 * i + 1]))

    mu_values = []
    f_values = []

    # Parse the mu and f(mu) pairs
    num_lines = int(np.ceil(2*NP/6))
    for i in range(start_idx + 2, start_idx + num_lines):
        line_values = parse_line(lines[i])
        mu_values.extend(line_values[::2])
        f_values.extend(line_values[1::2])

    end_idx = start_idx + 2 + num_lines
    return C1, C2, L1, L2, NR, NP, NBT, INT, mu_values, f_values, end_idx

def parse_TAB2(linechunk, start_index=0):
    """
    Parse a TAB2 chunk.
    
    Parameters:
        linechunk (list of str): Lines from the file.
        start_index (int): The starting index in the linechunk to read the TAB2 chunk.
        
    Returns:
        (int, int): NE2 (the number of following TAB1 chunks) and the new position.
    """
    # Parse the first line to get NE2
    first_line_values = parse_line(linechunk[start_index])
    NE2 = int(first_line_values[5])

    # Parse the second line (but do nothing with it)
    _ = parse_line(linechunk[start_index + 1])

    # Return NE2 and the new position
    return NE2, start_index + 2

def parse_LIST(linechunk, start_index=0):
    # Parse the first line to get C1 and NElements
    C1 = parse_line(linechunk[start_index])[1]
    NElements = parse_line(linechunk[start_index])[4]
    LIST_values = []

    # Number of lines to read
    num_lines = int(np.ceil(NElements/6)) + 1

    for i in range(start_index + 1, start_index + num_lines):
        line_values = parse_line(linechunk[i])
        LIST_values.extend(line_values)

    # Return C1, the parsed values, and the new position
    return C1, LIST_values, start_index + num_lines

def parse_line(line):
    # Extract the first 66 characters of the line
    data_section = line[:66]

    # Split the data into blocks of 11 characters
    blocks = re.findall(r'.{11}', data_section)

    # Convert each block to float using custom notation
    values = [custom_to_float(block) for block in blocks if block.strip()]

    return values


def find_target_block(file_path, targetMF, targetMT):
    block_lines = []
    inside_block = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            try:
                mat, mf, mt = parse_ID_line(line)
                if mf == targetMF and mt == targetMT:
                    inside_block = True
                    block_lines.append(line)
                else:
                    if inside_block:
                        # Exit the block when the condition is no longer met
                        break
            except ValueError:
                continue

    return block_lines

# Example function to save parsed data
def save_parsed_data(file_path, legendre_data, tabulated_data, ltt):
    with open(file_path, 'wb') as file:
        pickle.dump((legendre_data, tabulated_data, ltt), file)

# Example function to load parsed data
def load_parsed_data(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)
