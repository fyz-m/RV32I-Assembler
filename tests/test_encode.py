from src.encode import getType


def test_getType():
  assert getType("add s3, s1, s2") == "R-type"
  assert getType("addi s3, s1, 10") == "I-type"
  assert getType("sw s3, 12(s2)") == "S-type"
  assert getType("beq s3, s1, label") == "B-type"
  assert getType("lui s3, s1, 0xABCDEF") == "U-type"
  assert getType("jal ra, label") == "J-type" 