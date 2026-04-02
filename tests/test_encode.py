import src.encode
import pytest


def test_encode_R_type():
  assert src.encode.encode_R_type(op=51, rd=18, rs1=19, rs2=20, funct3=0, funct7=0) == 0x01498933
  assert src.encode.encode_R_type(op=51, rd=5, rs1=6, rs2=7, funct3=0, funct7=32) == 0x407302B3


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
  ...

def test_encode_B_type():
  ...

def test_encode_U_type():
  ...

def test_encode_J_type():
  ...
