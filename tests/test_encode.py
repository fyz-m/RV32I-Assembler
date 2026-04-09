import src.encode
import pytest
from src.Instruction import Instruction


def test_encode_R_type():
  # add s2, s3, s4
  assert src.encode.encode_R_type(op=51, rd=18, rs1=19, rs2=20, funct3=0, funct7=0) == 0x01498933
  # sub t0, t1, t2
  assert src.encode.encode_R_type(op=51, rd=5, rs1=6, rs2=7, funct3=0, funct7=32) == 0x407302B3
  # sll s7, t0, s1
  assert src.encode.encode_R_type(op=51, rd=23, rs1=5, rs2=9, funct3=1, funct7=0) == 0x00929BB3
   


def test_encode_I_type():
  # addi s0, s1, 12
  assert src.encode.encode_I_type(op=19, rd=8, rs1=9, funct3=0, imm=12) == 0x00C48413
  # addi s2, t1, -14
  assert src.encode.encode_I_type(op=19, rd=18, rs1=6, funct3=0, imm=-14) == 0xFF230913
  # lw t2, -6(s3)
  assert src.encode.encode_I_type(op=3, rd=7, rs1=19, funct3=2, imm=-6) == 0xFFA9A383
  # slli s2, s7, 5
  assert src.encode.encode_I_type(op=19, rd=18, rs1=23, funct3=1, imm=5) == 0x005B9913
  # srli s2, s7, 5
  assert src.encode.encode_I_type(op=19, rd=18, rs1=23, funct3=5, imm=5) == 0x005BD913
  # srai t1, t2, 29  
  assert src.encode.encode_I_type(op=19, rd=6, rs1=7, funct3=5, imm=29, funct7 = 0b0100000) == 0x41D3D313
  # xori x23, x21, 0xFFF
  assert src.encode.encode_I_type(op=19, rd=23, rs1=21, funct3=4, imm=0xFFF) == 0xFFFACB93

def test_encode_S_type():
  # sw t2, -6(s3)
  assert src.encode.encode_S_type(op=35, rs1=19, rs2=7, funct3=2, imm=-6) == 0xFE79AD23 
  # sh s4, 23(t0)
  assert src.encode.encode_S_type(op=35, rs1=5, rs2=20, funct3=1, imm=23) == 0x01429BA3 
  # sb t5, 0x2D(zero)
  assert src.encode.encode_S_type(op=35, rs1=0, rs2=30, funct3=0, imm=45) == 0x03E006A3 
  # sb t5, 0xFFFF(zero)
  assert src.encode.encode_S_type(op=35, rs1=0, rs2=30, funct3=0, imm=0xFFFF) == 0xFFE00FA3

def test_encode_B_type():
  # beq s0, t5, 16
  assert src.encode.encode_B_type(op=99, rs1=8, rs2=30, funct3=0, imm=16 ) == 0x01E40863
  # bne s8, s9, -2908
  assert src.encode.encode_B_type(op=99, rs1=24, rs2=25, funct3=1, imm=-2908 ) == 0xCB9C1263
  # beq s0, t5, 0x1FFF
  assert src.encode.encode_B_type(op=99, rs1=8, rs2=30, funct3=0, imm=0x1FFF ) == 0xFFE40FE3

def test_encode_U_type():
  # lui s5, 0x8CDEF
  assert src.encode.encode_U_type(op=55, rd=21, imm=0x8CDEF) == 0x8CDEFAB7
  # auipc x20, 0xFFFFF
  assert src.encode.encode_U_type(op=23, rd=20, imm=0xFFFFF) == 0xFFFFFA17

def test_encode_J_type():
  # jal x1, 0xA67F8
  assert src.encode.encode_J_type(op=111, rd=1, imm=0xA67F8) == 0x7F8A60EF
  # jal x1, 0x1FFFFF
  assert src.encode.encode_J_type(op=111, rd=1, imm=0x1FFFFF) == 0xFFFFF0EF

@pytest.mark.parametrize("input_inst, expected_encoding", [
  ("add s2, s3, s4",  0x01498933),
  ("addi x5, x6, 10", 0x00A30293),
  ("add x10, x11, x12", 0x00C58533),
  ("lui x15, 0xABCDE", 0xABCDE7B7),
  ("ori x1, x2, -1", 0xFFF16093),
  ("sub x7, x8, x9", 0x409403B3),
  ("slli x3, x4, 5", 0x00521193),
  ("srli s2, s7, 5",0x005BD913),
  ("srai t1, t2, 29",0x41D3D313),
  ("lw x20, 64(x21)", 0x040AAA03),
  ("lh x10, -128(x21)", 0xF80A9503),
  ("lb s4, 4(x1)", 0x00408A03),
  ("and x5, x6, x7", 0x007372B3),
  ("xori x30, x31, 255", 0x0FFFCF13),
  ("slt x1, x2, x3", 0x003120B3),
  ("bge x3, x4, 1024", 0x4041D063),
  ("bltu x6, x7, 8", 0x00736463),
  ("bgeu x15, x16, -100", 0xF907FEE3),

])

def test_encode(input_inst, expected_encoding):
  instruction = Instruction(input_inst)
  if instruction.type == "B-type" or instruction.type == "J-type":
    instruction.imm = int(instruction.label) #type:ignore

  assert src.encode.encode(instruction) == expected_encoding