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


'''@pytest.mark.parametrize("input_inst, expected_operands",[
        ("add s3, s1, s2", ["s3", "s1", "s2"] ),   
        ("addi s10, t0, 10", ["s10", "t0", "10"] ),  
        ("sw a0, 12(t5)", ["a0", "12(t5)"] ), 
        ("beq s11, zero, label", ["s11", "zero", "label"] ),  
        ("lui t6, 0xABCDEF", ["t6", "0xabcdef"] ),   
        ("jal ra, label", ["ra", "label"] ), 


])

def test_operands(input_inst, expected_operands):
  
  instruction = Instruction(input_inst)
  assert instruction.Operands == expected_operands '''


@pytest.mark.parametrize("input_inst", [
        ("add t0, zero, s1"),
  
])

def test_checkreg(input_inst):
  instruction = Instruction(input_inst)

  assert instruction.check_reg("s0") == True
  assert instruction.check_reg("ra") == True
  assert instruction.check_reg("fp") == True
  assert instruction.check_reg("sp") == True
  assert instruction.check_reg("s11") == True
  assert instruction.check_reg("x0") == True
  assert instruction.check_reg("x31") == True
  assert instruction.check_reg("t6") == True
  assert instruction.check_reg("a0") == True
  assert instruction.check_reg("x14") == True
  assert instruction.check_reg("x1") == True
  
  with pytest.raises(ValueError):
        assert instruction.check_reg("s1,s2")
        assert instruction.check_reg("s3 s4")

        assert instruction.check_reg(" s0")
        assert instruction.check_reg("S0")
        assert instruction.check_reg("S")
        assert instruction.check_reg("s12")
        assert instruction.check_reg(" s11 ")

        assert instruction.check_reg("0")
        assert instruction.check_reg("Zero")
        assert instruction.check_reg("ZERO")
        assert instruction.check_reg(" zero")
        assert instruction.check_reg(0)
        assert instruction.check_reg(13)

        assert instruction.check_reg("ra ")
        assert instruction.check_reg("r a")
        assert instruction.check_reg("r,a")
        assert instruction.check_reg("Ra")
        assert instruction.check_reg("RA")

        assert instruction.check_reg("x-3")
        assert instruction.check_reg("x32")
        assert instruction.check_reg("X1")
        assert instruction.check_reg(" X12")
        assert instruction.check_reg("x2 3")
        assert instruction.check_reg("x5 x6")
        assert instruction.check_reg("abcdef")
        assert instruction.check_reg("add x17")
        assert instruction.check_reg("zerox0")
        

def test_check_immediate_I_type():
   instruction = Instruction("add s1, s2, s3")
   instruction._Type = "I-type"

   assert instruction.check_Immediate(0) == True
   assert instruction.check_Immediate(23) == True 
   assert instruction.check_Immediate(-400) == True 
   assert instruction.check_Immediate(-4096) == True 
   assert instruction.check_Immediate(4095) == True 

   with pytest.raises(ValueError):
      assert instruction.check_Immediate(20000)
      assert instruction.check_Immediate(4096)
      assert instruction.check_Immediate(-4097)

def test_check_immediate_I_type_shift():
   instruction = Instruction("add s1, s2, s3")
   instruction._Type = "I-type"
   instruction._Mnemonic = "slli"

   assert instruction.check_Immediate(0) == True
   assert instruction.check_Immediate(23) == True 
   assert instruction.check_Immediate(32) == True 
   assert instruction.check_Immediate(31) == True 
   

   with pytest.raises(ValueError):
      assert instruction.check_Immediate(33)
      assert instruction.check_Immediate(400)
      assert instruction.check_Immediate(-1)
      assert instruction.check_Immediate(-31)
      assert instruction.check_Immediate(-32)
       


  

@pytest.mark.parametrize("input_inst",[
        ("add s3, s1, s2"),   
        ("addi s3, s1, 10"),  
        ("sw s3, 12(s2)"), 
        ("beq s3, s1, label"),  
        ("lui s3, 0xABCDEF"),   
        ("jal ra, label"), 


])

def test_extract_operands(input_inst):
  instruction = Instruction(input_inst)
  assert instruction.extract_operands() == True
  