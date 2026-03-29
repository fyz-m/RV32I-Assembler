from src.Instruction import Instruction
import pytest

@pytest.mark.parametrize("input_inst, expected_mnemonic, expected_type",[
        ("add s3, s1, s2",  "add", "R-type"),   
        ("addi s3, s1, 10", "addi", "I-type"),  
        ("sw s3, 12(s2)", "sw", "S-type"), 
        ("beq s3, s1, label", "beq", "B-type"),  
        ("lui s3, 0xABCDEF)", "lui", "U-type"),   
        ("jal ra, label", "jal", "J-type"), 


])

def test_mnemonic_type(input_inst, expected_mnemonic, expected_type):
  instruction = Instruction(input_inst)
  assert instruction.Mnemonic == expected_mnemonic
  assert instruction.Type == expected_type


@pytest.mark.parametrize("input_inst, expected_operands",[
        ("add s3, s1, s2", ["s3", "s1", "s2"] ),   
        ("addi s10, t0, 10", ["s10", "t0", "10"] ),  
        ("sw a0, 12(t5)", ["a0", "12(t5)"] ), 
        ("beq s11, zero, label", ["s11", "zero", "label"] ),  
        ("lui t6, 0xABCDEF", ["t6", "0xABCDEF"] ),   
        ("jal ra, label", ["ra", "label"] ), 


])

def test_operands(input_inst, expected_operands):
  
  instruction = Instruction(input_inst)
  assert instruction.Operands == expected_operands


@pytest.mark.parametrize("input_inst, expected_registers", [
        ("add t0, zero, s1", {"rd":5 , "rs1":0, "rs2":9}),
        ("addi zero, zero, 0", {"rd":0 , "rs1":0,}),
        ("sw t5, 20(s3)", {"rs2":30, "rs1":19 })
  
])

def test_Registers(input_inst, expected_registers):
  
  instruction = Instruction(input_inst)
  assert instruction.Registers == expected_registers

