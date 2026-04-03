from src.Instruction import Instruction, InstructionError
import pytest


@pytest.mark.parametrize("input_inst", [
        ("add123"),
        ("xors1s2s3"),
        ("instruction"),
        (" "),
        ("#Comment"),
])

def test_instruction_setter_error(input_inst):
    
    with pytest.raises(InstructionError):
      instruction = Instruction(input_inst)

@pytest.mark.parametrize("input_inst, expected_mnemonic", [
        ("add t0, zero, s1", "add"),
        ("ADD t0, zero, s1", "add"),
        (" ADD   t0, zero, s1", "add"),
        ("LUI   t0, 0", "lui"),
        (" SlTu s3, s4, t1", "sltu"),
        (" Sw x0, 5(x1)", "sw"),
        
  
])

def test_mnemonic_setter(input_inst, expected_mnemonic):
    instruction = Instruction(input_inst)
    assert instruction.Mnemonic == expected_mnemonic

@pytest.mark.parametrize("input_inst", [
        ("fmadd t0, zero, s1"),
        ("addinstruction t0, zero, s1"),
        ("addition   t0, zero, s1"),
        ("ld t0, 0"),
        ("ad d SlTu s3, s4, t1"),
        ("mnemonic s1, s2, s3"),
        
])

def test_mnemonic_setter_error(input_inst):
    
    with pytest.raises(InstructionError):
      instruction = Instruction(input_inst)
        
def test_checkreg():
  instruction = Instruction("add t0, zero, s1")

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
        ("addi s3, s1, -15", {"rs1":9, "rs2":None, "rd":19, "imm":-15} ),
        ("sw s3, 12(s2)", {"rs1":18, "rs2":19, "rd":None, "imm":12} ), 
        ("sw s3, -80(s2)", {"rs1":18, "rs2":19, "rd":None, "imm":-80} ),
        ("beq s3, s1, 47", {"rs1":19, "rs2":9, "rd":None, "imm":47} ),  
        ("beq s3, s1, -47", {"rs1":19, "rs2":9, "rd":None, "imm":-47} ), 
        ("lui s3, 0xFFFFF", {"rs1":None, "rs2":None, "rd":19, "imm":1048575} ),
        ("lui s3, -400", {"rs1":None, "rs2":None, "rd":19, "imm":-400} ),   
        ("jal ra, 0b1011", {"rs1":None, "rs2":None, "rd":1, "imm":11} ),
        ("jal ra, -80", {"rs1":None, "rs2":None, "rd":1, "imm":-80} ), 

        ("add  S3 ,s1,    s2", {"rs1":9, "rs2":18, "rd":19, "imm":None} ),   
        ("addi     s3, s1   , 10", {"rs1":9, "rs2":None, "rd":19, "imm":10} ),  
        ("sw s3, 12(s2)", {"rs1":18, "rs2":19, "rd":None, "imm":12} ), 
        ("sw   t0   ,    10(x1)", {"rs1":1, "rs2":5, "rd":None, "imm":10} ),
        ("beq   s3 , s1, 47", {"rs1":19, "rs2":9, "rd":None, "imm":47} ),  
        ("lui s3,0xFFFFF", {"rs1":None, "rs2":None, "rd":19, "imm":1048575} ),   
        ("jal ra,0b1011", {"rs1":None, "rs2":None, "rd":1, "imm":11} ), 


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
  
@pytest.mark.parametrize("input_inst",[
        ("adds1, s2, s3"),
        ("beqx31,a0, 0"),
        ("sw t0, 10 ( x1 )"),
        ("sw t0, 1( x1 )"),
        ("sw t0, 12 (x5)"),
        ("add t0, s1"),
        ("subi t1, 40"),
        ("xor s3 s1 t3"),
        ("jal 0xABC"),
        ("lui s13 400"),
        ("add addi x1, x3, x4"),
        ("beq   xor, x3, add")

])

def test_extract_operands_Error(input_inst):

    with pytest.raises(InstructionError):
        instruction = Instruction(input_inst)
    
@pytest.mark.parametrize("input_inst, expected_op, expected_funct3, expected_funct7",[
    
        ("add x1, x1, x1", 51, 0, 0),
        ("sub x1, x1, x1", 51, 0, 32),
        ("srl x1, x1, x1", 51, 5, 0),
        ("sra x1, x1, x1", 51, 5, 32),

        ("sw x1, 0(x1)", 35, 2, None),
        ("xori x1, x1, 0", 19, 4, None),
        ("slli x1, x1, 0", 19, 1, 0),
        ("srai x1, x1, 0", 19, 5, 32),

        ("bltu x1, x1, 20", 99, 6, None),
        ("jal ra, 20", 111, None , None),       
])

def test_controlbits(input_inst, expected_op, expected_funct3, expected_funct7):
    instruction = Instruction(input_inst)
   
    assert instruction.op == expected_op
    assert instruction.funct3 == expected_funct3
    assert instruction.funct7 == expected_funct7