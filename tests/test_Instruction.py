from src.Instruction import Instruction
import pytest

@pytest.mark.parametrize("input_inst, expected_mnemonic, expected_type",[
        ("add s3, s1, s2",  "add", "R-type"),   
        ("addi s3, s1, 10", "addi", "I-type"),  
        ("sw s3, 12(s2)", "sw", "S-type"), 
        ("beq s3, s1, label", "beq", "B-type"),  
        ("lui s3, s1, 0xABCDEF)", "lui", "U-type"),   
        ("jal ra, label", "jal", "J-type"), 


])

def test_mnemonic_type(input_inst, expected_mnemonic, expected_type):
  instruction = Instruction(input_inst)
  assert instruction.Mnemonic == expected_mnemonic
  assert instruction.Type == expected_type


