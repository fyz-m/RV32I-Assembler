from src.Instruction import Instruction, InstructionError
import pytest

'''@pytest.mark.parametrize("input_inst, expected_mnemonic, expected_type",[
        ("add s3, s1, s2",  "add", "R-type"),   
        ("addi s3, s1, 10", "addi", "I-type"),  
        ("sw s3, 12(s2)", "sw", "S-type"), 
        ("beq s3, s1, label", "beq", "B-type"),  
        ("lui s3, 0xABCDEF", "lui", "U-type"),   
        ("jal ra, label", "jal", "J-type"), 


])

def test_mnemonic_type(input_inst, expected_mnemonic, expected_type):
  instruction = Instruction(input_inst)
  assert instruction.Mnemonic == expected_mnemonic
  assert instruction.Type == expected_type
'''


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
  
  with pytest.raises(InstructionError):
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
        
def test_immediate_setter():
   instruction = Instruction("add s1, s2, s3")
   instruction._Type = "I-type"

   instruction.imm = "0xABC"
   instruction.imm = "0b10011"
   instruction.imm = "0XABC"
   instruction.imm = "0B10011"

   with pytest.raises(InstructionError):
       instruction.imm = "Integer"
       instruction.imm = "ABC"
       instruction.imm = "1011"
       instruction.imm = "0xHexadecimal"
       instruction.imm = "12.5"
       instruction.imm = "100.1"
       instruction.imm = "-200.5"
       instruction.imm = "0b110.1"
    
def test_check_immediate_I_S_type():
   instruction = Instruction("add s1, s2, s3")
   instruction._Type = "I-type"
   
   assert instruction.check_Immediate(0) == True
   assert instruction.check_Immediate(23) == True 
   assert instruction.check_Immediate(-400) == True 
   assert instruction.check_Immediate(-4096) == True 
   assert instruction.check_Immediate(4095) == True 

   with pytest.raises(InstructionError):
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
   

   with pytest.raises(InstructionError):
      assert instruction.check_Immediate(33)
      assert instruction.check_Immediate(400)
      assert instruction.check_Immediate(-1)
      assert instruction.check_Immediate(-31)
      assert instruction.check_Immediate(-32)
       
def test_check_immediate_B_type():
   instruction = Instruction("add s1, s2, s3")
   instruction._Type = "B-type"

   assert instruction.check_Immediate(0) == True
   assert instruction.check_Immediate(8191) == True
   assert instruction.check_Immediate(-8192) == True

   with pytest.raises(InstructionError):
      assert instruction.check_Immediate(8192)
      assert instruction.check_Immediate(8200)      
      assert instruction.check_Immediate(-8193)
      assert instruction.check_Immediate(-20000)

def test_check_immediate_U_type():
   instruction = Instruction("add s1, s2, s3")
   instruction._Type = "U-type"

   assert instruction.check_Immediate(0) == True
   assert instruction.check_Immediate(1048575) == True
   assert instruction.check_Immediate(-1048576) == True
   assert instruction.check_Immediate(1048574) == True
   assert instruction.check_Immediate(-1048575) == True

   with pytest.raises(InstructionError):
      assert instruction.check_Immediate(1048576)
      assert instruction.check_Immediate(-1048577)      
      assert instruction.check_Immediate(-10000000)
      assert instruction.check_Immediate(2400000)  

def test_check_immediate_J_type():
   instruction = Instruction("add s1, s2, s3")
   instruction._Type = "J-type"

   assert instruction.check_Immediate(0) == True
   assert instruction.check_Immediate(40000) == True
   assert instruction.check_Immediate(2097151) == True
   assert instruction.check_Immediate(-2097152) == True
   assert instruction.check_Immediate(2097150) == True
   assert instruction.check_Immediate(-2097151) == True

   with pytest.raises(InstructionError):
      assert instruction.check_Immediate(2097152)
      assert instruction.check_Immediate(-2097153)      
      assert instruction.check_Immediate(-10000000)
      assert instruction.check_Immediate(2400000)  

@pytest.mark.parametrize("input_inst, expected_operands",[
        ("add s3, s1, s2", {"rs1":9, "rs2":18, "rd":19, "imm":None} ),   
        ("addi s3, s1, 10", {"rs1":9, "rs2":None, "rd":19, "imm":10} ),  
        ("sw s3, 12(s2)", {"rs1":18, "rs2":19, "rd":None, "imm":12} ), 
        ("beq s3, s1, 47", {"rs1":19, "rs2":9, "rd":None, "imm":47} ),  
        ("lui s3, 0xFFFFF", {"rs1":None, "rs2":None, "rd":19, "imm":1048575} ),   
        ("jal ra, 0b1011", {"rs1":None, "rs2":None, "rd":1, "imm":11} ), 


])

def test_extract_operands(input_inst, expected_operands):
  instruction = Instruction(input_inst)
  assert instruction.extract_operands() == True
  if expected_operands['rs1']:
        assert instruction.rs1 == expected_operands['rs1']
  if expected_operands['rs2']:
        assert instruction.rs2 == expected_operands['rs2']
  if expected_operands['rd']:
        assert instruction.rd == expected_operands['rd']
  if expected_operands['imm']:
        assert instruction.imm == expected_operands['imm']
  