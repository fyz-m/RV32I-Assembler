from src.Instruction import Instruction
import pytest

@pytest.mark.parametrize("input_inst, expected_mnemonic",[
        ("add s3, s1, s2",  "add"),   
        ("addi s3, s1, 10", "addi"),  
        ("sw s3, 12(s2)", "sw"), 
        ("beq s3, s1, label", "beq"),  
        ("lui s3, s1, 0xABCDEF)", "lui"),   
        ("jal ra, label", "jal"), 


])

def test_mnemonic(input_inst, expected_mnemonic):
  instruction = Instruction(input_inst)
  assert instruction.Mnemonic == expected_mnemonic


@pytest.mark.parametrize("input_inst, expected_type", [
        ("add s3, s1, s2",  "R-type"),   
        ("addi s3, s1, 10", "I-type"),  
        ("sw s3, 12(s2)", "S-type"), 
        ("beq s3, s1, label", "B-type"),  
        ("lui s3, s1, 0xABCDEF)", "U-type"),   
        ("jal ra, label", "J-type"), 
    ])

def test_type(input_inst, expected_type):
  instruction = Instruction(input_inst)
  assert instruction.Type == expected_type

