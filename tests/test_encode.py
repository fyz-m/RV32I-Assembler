from src.encode import Instruction


def test_getType():
  instruction = Instruction("add s3, s1, s2")
  assert instruction.Type == "R-type"
  del instruction
  
  instruction = Instruction("addi s3, s1, 10") 
  assert instruction.Type == "I-type"
  del instruction
  
  instruction = Instruction("sw s3, 12(s2)") 
  assert instruction.Type == "S-type"
  del instruction
  
  instruction = Instruction("beq s3, s1, label") 
  assert instruction.Type == "B-type"
  del instruction
  
  instruction = Instruction("lui s3, s1, 0xABCDEF") 
  assert instruction.Type == "U-type"
  del instruction
  
  instruction = Instruction("jal ra, label") 
  assert instruction.Type == "J-type"
  del instruction
  