
def encode(inst):

    """
    Dispatch an Instruction object to the correct encoding function

    Args:
        inst: Instruction object with fields: type, op, rd, rs1, rs2, funct3, funct7, imm

    Returns:
        32-bit encoded instruction as an integer

    """

    match inst.type:
        case "R-type":
            return encode_R_type(inst.op, inst.rd, inst.rs1, inst.rs2, inst.funct3, inst.funct7)
        case "I-type":
            return encode_I_type(inst.op, inst.rd, inst.rs1, inst.funct3, inst.imm, inst.funct7)
        case "S-type":
            return encode_S_type(inst.op, inst.rs1, inst.rs2, inst.funct3, inst.imm)
        case "B-type":
            return encode_B_type(inst.op, inst.rs1, inst.rs2, inst.funct3, inst.imm)
        case "U-type":
            return encode_U_type(inst.op, inst.rd, inst.imm)
        case "J-type":
            return encode_J_type(inst.op, inst.rd, inst.imm)




def encode_R_type(op: int, rd: int, rs1: int, rs2: int, funct3: int, funct7: int) -> int:
    """
    Encode R-type instruction into a 32-bit integer

    Bit layout:
    | funct7 |  rs2   |  rs1   | funct3 |   rd   |   op   |
    |  7-bit |  5-bit |  5-bit |  3-bit |  5-bit |  7-bit |

    """
    return (
        op
        | rd << 7 
        | funct3 << 12
        | rs1 << 15
        | rs2 << 20
        | funct7 << 25
    )
   


def encode_I_type(op: int, rd: int, rs1: int, funct3: int, imm: int, funct7=None) -> int:
    """
    Encode an I-type instruction into a 32-bit integer

    Bit layout:
    |  imm[11:0]  |  rs1   | funct3 |   rd   |   op   |
    |   12-bit    |  5-bit |  3-bit |  5-bit |  7-bit |

    """

    # Sign extend immediate to 12 bits
    imm = imm & 0xFFF

    
    # Shift immediates are 5-bit, upper bits of immediate = funct7 in shift instructions
    # srli and srai share opcode and funct3, so they are differentiated by srai having funct7 = 0b0100000, or imm[10] = 1
    # If instruction is srai, imm[10] should be set
    if funct7 == 32:
        imm = imm | (1 << 10)

    return (
        op
        | rd << 7
        | funct3 << 12
        | rs1 << 15
        | imm << 20
    )



def encode_S_type(op: int, rs1: int, rs2: int, funct3: int, imm: int) -> int:
    """
    Encode an S-type instruction into a 32-bit integer

    Bit layout:
    | imm[11:5] |  rs2   |  rs1   | funct3 | imm[4:0] |   op   |
    |   7-bit   |  5-bit |  5-bit |  3-bit |   5-bit  |  7-bit |

    """
    # Sign extend immediate to 12 bits
    imm = imm & 0xFFF

    # Extract imm[4:0]
    imm_4_0 = imm & 0x01F  # mask = 0000_0001_1111

    # Extract imm[11:5]
    imm_11_5 = imm >> 5

    return (
        op
        | funct3 << 12
        | imm_4_0 << 7
        | rs1 << 15
        | rs2 << 20
        | imm_11_5 << 25
    )
    


def encode_B_type(op: int, rs1: int, rs2: int, funct3: int, imm: int) -> int:
    """
    Encode a B-type instruction into a 32-bit integer

    Bit layout:
    | imm[12] | imm[10:5] |  rs2   |  rs1   | funct3 | imm[4:1] | imm[11] |   op   |
    |  1-bit  |   6-bit   |  5-bit |  5-bit |  3-bit |   4-bit  |  1-bit  |  7-bit |

    The immediate encoding is designed to minimize the hardware for extracting and sign extending it
    RISC-V tries to keep the immediate bits location as consistent as possible across instruction types
    """
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

    return (
        op
        | imm_11 << 7
        | imm_4_1 << 8
        | funct3 << 12
        | rs1 << 15
        | rs2 << 20
        | imm_10_5 << 25
        | imm_12 << 31
    )



def encode_U_type(op: int, rd: int, imm: int) -> int:
    """
    Encode a U-type instruction into a 32-bit integer

    Bit layout:
    | imm[31:12] |   rd   |   op   |
    |   20-bit   |  5-bit |  7-bit |

    """
    # Extend immediate to 20-bit
    imm = imm & 0xFFFFF

    return (imm << 12) | (rd << 7) | op

    


def encode_J_type(op: int, rd: int, imm: int) -> int:
    """
    Encode a J-type instruction into a 32-bit integer

    Bit layout:
    | imm[20] | imm[10:1] | imm[11] | imm[19:12] |   rd   |   op  |
    |                   12-bit                   |  5-bit | 7-bit |

    """
    # Extend immediate to 21-bit
    imm = imm & 0x1FFFFF

    # Extract imm[10:1]
    # As with B-type instructions, imm[0] is not encoded
    imm_10_1 = (imm >> 1) & 0x003FF  

    # Extract imm[11]
    imm_11 = (imm >> 11) & 0x01 

    # Extract imm[19:12]
    imm_19_12 = (imm >> 12) & 0xFF 

    # Extract imm[20]
    imm_20 = imm >> 20

    return (
        op
        | rd << 7
        | imm_19_12 << 12
        | imm_11 << 20
        | imm_10_1 << 21
        | imm_20 << 31
    )
