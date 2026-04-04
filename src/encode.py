# TODO:
# Clean up code
# Comments and docstrings
def encode(inst):
    """
    Takes Instruction object as input (contains field values like opcode and registers)
    Returns encoded instruction as 32-bit integer
    """

    match inst.Type:
        case "R-type":
            return encode_R_type(inst.op, inst.rd, inst.rs1, inst.rs2, inst.funct3, inst.funct7)
        case "I-type":
            return encode_I_type(inst.op, inst.rd, inst.rs1, inst.funct3, inst.imm)
        case "S-type":
            return encode_S_type(inst.op, inst.rs1, inst.rs2, inst.funct3, inst.imm)
        case "B-type":
            return encode_B_type(inst.op, inst.rs1, inst.rs2, inst.funct3, inst.imm)
        case "U-type":
            return encode_U_type(inst.op, inst.rd, inst.imm)
        case "J-type":
            return encode_J_type(inst.op, inst.rd, inst.imm)


"""
  All encoding functions take fields input as integers
"""


def encode_R_type(op, rd, rs1, rs2, funct3, funct7):
    """
    R-type instruction are encoded as the following:

    bit[6:0] = opcode
    bit[11:7] = destination register (rd)
    bit[14:12] = function field 3
    bit[19:15] = source register 1 (rs1)
    bit[24:20] = source register 2 (rs2)
    bit[31:25] = function field 7

    """
    # Shift the value to its starting bit postion, pad with zeroes
    rd = rd << 7  # rd = rd_000_0000
    funct3 = funct3 << 12
    rs1 = rs1 << 15
    rs2 = rs2 << 20
    funct7 = funct7 << 25

    return op | rd | funct3 | rs1 | rs2 | funct7


def encode_I_type(op, rd, rs1, funct3, imm):
    """
    I-type instruction are encoded as the following:

    bit[6:0] = opcode
    bit[11:7] = destination register (rd)
    bit[14:12] = function field 3
    bit[19:15] = source register 1 (rs1)
    bit[31:20] = Immediate

    """

    # Sign extend immediate to 12 bits
    imm = imm & 0xFFF

    # If instruction is srai, imm[10] should be set
    if op == 19 and funct3 == 5:
        imm = imm | 1 << 10

    rd = rd << 7
    funct3 = funct3 << 12
    rs1 = rs1 << 15
    imm = imm << 20

    return op | rd | funct3 | rs1 | imm


def encode_S_type(op, rs1, rs2, funct3, imm):
    """ """
    # Sign extend immediate to 12 bits
    imm = imm & 0xFFF

    # Extract imm[4:0]
    imm_4_0 = imm & 0x01F  # mask = 0000_0001_1111

    # Extract imm[11:5]
    imm_11_5 = imm >> 5

    funct3 = funct3 << 12
    rs1 = rs1 << 15
    rs2 = rs2 << 20
    imm_4_0 = imm_4_0 << 7
    imm_11_5 = imm_11_5 << 25

    return op | rs1 | rs2 | funct3 | imm_11_5 | imm_4_0


def encode_B_type(op, rs1, rs2, funct3, imm):
    """ """
    # Sign extend immediate to 13 bits
    # B-type instructions have a 13-bit immediate since branch offset is always a multiple of 4, instruction are 4-bytes apart.
    # Therefore imm[1:0] are always 0
    # imm[0] is discarded to fit the immediate in the 12-bit field
    # imm[1] can also be discarded but is still encoded for compatibility with compressed RISC-V instructions
    imm = imm & 0x1FFF

    # Extract imm[4:1]
    imm_4_1 = (imm >> 1) & 0x00F  # 0000_0000_1111

    # Extract imm[10:5]
    imm_10_5 = (imm >> 5) & 0b00_1111_11

    # Extract imm[11]
    imm_11 = (imm >> 11) & 0b01

    # Extract imm[12]
    imm_12 = imm >> 12

    # Shift fields to their respective location in the 32-bit instruction
    funct3 = funct3 << 12
    rs1 = rs1 << 15
    rs2 = rs2 << 20

    imm_11 = imm_11 << 7
    imm_4_1 = imm_4_1 << 8
    imm_10_5 = imm_10_5 << 25
    imm_12 = imm_12 << 31

    return op | rs1 | rs2 | funct3 | imm_11 | imm_4_1 | imm_10_5 | imm_12


def encode_U_type(op, rd, imm):
    """
    Encodes U-type instruction into a 32-bit integer

    Format:
    | imm[31:12] |   rd   |   op  |
    |   12-bit   |  5-bit | 7-bit |

    """
    # Extend immediate to 20-bit
    imm = imm & 0xFFFFF

    rd = rd << 7
    imm = imm << 12

    return op | rd | imm


def encode_J_type(op, rd, imm):
    """
    Encodes J-type instruction into a 32-bit integer

    Format:
    | imm[20] | imm[10:1] | imm[11] | imm[19:12] |   rd   |   op  |
    |                   12-bit                   |  5-bit | 7-bit |

    """
    # Extend immediate to 21-bit
    imm = imm & 0x1FFFFF

    # Extract imm[10:1]
    imm_10_1 = (imm >> 1) & 0x003FF  # 0000_0000_0011_1111_1111
    # Extract imm[11]
    imm_11 = (imm >> 11) & 0x01  # 0000_0001
    # Extract imm[19:12]
    imm_19_12 = (imm >> 12) & 0x1FF  # 0001_1111_1111
    # Extract imm[20]
    imm_20 = imm >> 20

    rd = rd << 7
    imm_19_12 = imm_19_12 << 12
    imm_11 = imm_11 << 20
    imm_10_1 = imm_10_1 << 21
    imm_20 = imm_20 << 31

    return op | rd | imm_19_12 | imm_11 | imm_10_1 | imm_20
