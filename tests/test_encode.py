import src.encode
import pytest

def test_encode_R_type():
  assert src.encode.encode_R_type(op=51, rd=18, rs1=19, rs2=20, funct3=0, funct7=0) == 0x01498933
  assert src.encode.encode_R_type(op=51, rd=5, rs1=6, rs2=7, funct3=0, funct7=32) == 0x407302B3


def test_encode_I_type():
  ...

def test_encode_S_type():
  ...

def test_encode_B_type():
  ...

def test_encode_U_type():
  ...

def test_encode_J_type():
  ...
