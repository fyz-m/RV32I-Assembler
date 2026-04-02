import src.encode
import pytest


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
  # srai t1, t2, 29  
  assert src.encode.encode_I_type(op=19, rd=6, rs1=7, funct3=5, imm=29) == 0x41D3D313
 
def test_encode_S_type():
  # sw t2, -6(s3)
  assert src.encode.encode_S_type(op=35, rs1=19, rs2=7, funct3=2, imm=-6) == 0xFE79AD23 
  # sh s4, 23(t0)
  assert src.encode.encode_S_type(op=35, rs1=5, rs2=20, funct3=1, imm=23) == 0x01429BA3 
  # sb t5, 0x2D(zero)
  assert src.encode.encode_S_type(op=35, rs1=0, rs2=30, funct3=0, imm=45) == 0x03E006A3 

def test_encode_B_type():
  # beq s0, t5, 16
  assert src.encode.encode_B_type(op=99, rs1=8, rs2=30, funct3=0, imm=16 ) == 0x01E40863
  # bne s8, s9, -2908
  assert src.encode.encode_B_type(op=99, rs1=24, rs2=25, funct3=1, imm=-2908 ) == 0xCB9C1263

def test_encode_U_type():
  # lui s5, 0x8CDEF
  assert src.encode.encode_U_type(op=55, rd=21, imm=0x8CDEF) == 0x8CDEFAB7

def test_encode_J_type():
  # jal x1, 0xA67F8
  assert src.encode.encode_J_type(op=111, rd=1, imm=0xA67F8) == 0x7F8A60EF
