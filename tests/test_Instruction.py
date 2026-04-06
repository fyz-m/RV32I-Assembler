#type: ignore
from src.Instruction import Instruction, InstructionError
import pytest


@pytest.mark.parametrize("input_inst", [
        ("add123"),
        ("xors1s2s3"),
        ("instruction"),
        (" "),
        ("#Comment"),
])

def test_parse_instruction_error(input_inst):
    
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

def test_parse_mnemonic(input_inst, expected_mnemonic):
    instruction = Instruction(input_inst)
    assert instruction.mnemonic == expected_mnemonic

@pytest.mark.parametrize("input_inst", [
        ("fmadd t0, zero, s1"),
        ("addinstruction t0, zero, s1"),
        ("addition   t0, zero, s1"),
        ("ld t0, 0"),
        ("ad d SlTu s3, s4, t1"),
        ("mnemonic s1, s2, s3"),
        
])

def test_parse_mnemonic_error(input_inst):
    
    with pytest.raises(InstructionError):
      instruction = Instruction(input_inst)
        
def test_checkreg():
  instruction = Instruction("add t0, zero, s1")

  assert instruction.check_register("s0") == True
  assert instruction.check_register("ra") == True
  assert instruction.check_register("fp") == True
  assert instruction.check_register("sp") == True
  assert instruction.check_register("s11") == True
  assert instruction.check_register("x0") == True
  assert instruction.check_register("x31") == True
  assert instruction.check_register("t6") == True
  assert instruction.check_register("a0") == True
  assert instruction.check_register("x14") == True
  assert instruction.check_register("x1") == True
  
  with pytest.raises(InstructionError):
        assert instruction.check_register("s1,s2")
        assert instruction.check_register("s3 s4")

        assert instruction.check_register(" s0")
        assert instruction.check_register("S0")
        assert instruction.check_register("S")
        assert instruction.check_register("s12")
        assert instruction.check_register(" s11 ")

        assert instruction.check_register("0")
        assert instruction.check_register("Zero")
        assert instruction.check_register("ZERO")
        assert instruction.check_register(" zero")
        assert instruction.check_register(0)
        assert instruction.check_register(13)

        assert instruction.check_register("ra ")
        assert instruction.check_register("r a")
        assert instruction.check_register("r,a")
        assert instruction.check_register("Ra")
        assert instruction.check_register("RA")

        assert instruction.check_register("x-3")
        assert instruction.check_register("x32")
        assert instruction.check_register("X1")
        assert instruction.check_register(" X12")
        assert instruction.check_register("x2 3")
        assert instruction.check_register("x5 x6")
        assert instruction.check_register("abcdef")
        assert instruction.check_register("add x17")
        assert instruction.check_register("zerox0")
        
def test_immediate_setter():
   instruction = Instruction("add s1, s2, s3")
   instruction.type = "I-type"

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
   instruction.type = "I-type"
   
   assert instruction.check_immediate(0) == True
   assert instruction.check_immediate(23) == True 
   assert instruction.check_immediate(-400) == True 
   assert instruction.check_immediate(-4096) == True 
   assert instruction.check_immediate(4095) == True 

   with pytest.raises(InstructionError):
      assert instruction.check_immediate(20000)
      assert instruction.check_immediate(4096)
      assert instruction.check_immediate(-4097)

def test_check_immediate_I_type_shift():
   instruction = Instruction("add s1, s2, s3")
   instruction.type = "I-type"
   instruction.mnemonic = "slli"

   assert instruction.check_immediate(0) == True
   assert instruction.check_immediate(23) == True 
   assert instruction.check_immediate(32) == True 
   assert instruction.check_immediate(31) == True 
   

   with pytest.raises(InstructionError):
      assert instruction.check_immediate(33)
      assert instruction.check_immediate(400)
      assert instruction.check_immediate(-1)
      assert instruction.check_immediate(-31)
      assert instruction.check_immediate(-32)
       
def test_check_immediate_B_type():
   instruction = Instruction("add s1, s2, s3")
   instruction.type = "B-type"

   assert instruction.check_immediate(0) == True
   assert instruction.check_immediate(8191) == True
   assert instruction.check_immediate(-8192) == True

   with pytest.raises(InstructionError):
      assert instruction.check_immediate(8192)
      assert instruction.check_immediate(8200)      
      assert instruction.check_immediate(-8193)
      assert instruction.check_immediate(-20000)

def test_check_immediate_U_type():
   instruction = Instruction("add s1, s2, s3")
   instruction.type = "U-type"

   assert instruction.check_immediate(0) == True
   assert instruction.check_immediate(1048575) == True
   assert instruction.check_immediate(-1048576) == True
   assert instruction.check_immediate(1048574) == True
   assert instruction.check_immediate(-1048575) == True

   with pytest.raises(InstructionError):
      assert instruction.check_immediate(1048576)
      assert instruction.check_immediate(-1048577)      
      assert instruction.check_immediate(-10000000)
      assert instruction.check_immediate(2400000)  

def test_check_immediate_J_type():
   instruction = Instruction("add s1, s2, s3")
   instruction.type = "J-type"

   assert instruction.check_immediate(0) == True
   assert instruction.check_immediate(40000) == True
   assert instruction.check_immediate(2097151) == True
   assert instruction.check_immediate(-2097152) == True
   assert instruction.check_immediate(2097150) == True
   assert instruction.check_immediate(-2097151) == True

   with pytest.raises(InstructionError):
      assert instruction.check_immediate(2097152)
      assert instruction.check_immediate(-2097153)      
      assert instruction.check_immediate(-10000000)
      assert instruction.check_immediate(2400000)  

@pytest.mark.parametrize("input_inst, expected_operands",[
        ("add s3, s1, s2", {"rs1":9, "rs2":18, "rd":19, "imm":None, "label":None} ),   
        ("addi s3, s1, 10", {"rs1":9, "rs2":None, "rd":19, "imm":10, "label":None} ), 
        ("addi s3, s1, -15", {"rs1":9, "rs2":None, "rd":19, "imm":-15, "label":None} ),
        ("sw s3, 12(s2)", {"rs1":18, "rs2":19, "rd":None, "imm":12, "label":None} ), 
        ("sw s3, -80(s2)", {"rs1":18, "rs2":19, "rd":None, "imm":-80, "label":None} ),
        ("beq s3, s1, 47", {"rs1":19, "rs2":9, "rd":None, "imm":None, "label":"47"} ),  
        ("beq s3, s1, -47", {"rs1":19, "rs2":9, "rd":None, "imm":None, "label":"-47"} ), 
        ("lui s3, 0xFFFFF", {"rs1":None, "rs2":None, "rd":19, "imm":1048575, "label":None} ),
        ("lui s3, -400", {"rs1":None, "rs2":None, "rd":19, "imm":-400, "label":None} ),   
    
        ("add  S3 ,s1,    s2", {"rs1":9, "rs2":18, "rd":19, "imm":None, "label":None} ),   
        ("addi     s3, s1   , 10", {"rs1":9, "rs2":None, "rd":19, "imm":10, "label":None} ),  
        ("sw s3, 12(s2)", {"rs1":18, "rs2":19, "rd":None, "imm":12, "label":None} ), 
        ("sw   t0   ,    10(x1)", {"rs1":1, "rs2":5, "rd":None, "imm":10, "label":None} ),
        ("beq   s3 , s1, jump", {"rs1":19, "rs2":9, "rd":None, "imm":None, "label":"jump"} ),  
        ("lui s3,0xFFFFF", {"rs1":None, "rs2":None, "rd":19, "imm":1048575, "label":None} ),   
        ("jal ra,0b1011", {"rs1":None, "rs2":None, "rd":1, "imm":None, "label":"0b1011"} ),
        ("jal ra, loop", {"rs1":None, "rs2":None, "rd":1, "imm":None, "label":'loop'} ), 

        ("lw x20, 64(x21)", {"rs1":21, "rs2":None, "rd":20, "imm":64, "label":None} ),
        ("lh x8, -800(x14)", {"rs1":14, "rs2":None, "rd":8, "imm":-800, "label":None} ),
        ("lb x1, 4(x1)", {"rs1":1, "rs2":None, "rd":1, "imm":4, "label":None} ),


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
  if expected_operands['label']:
        assert instruction.label == expected_operands['label']
  
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

@pytest.mark.parametrize("input_inst, valid_inst, expected_operands",[
        ("add s3, s1, s2", True, {"rs1":9, "rs2":18, "rd":19, "imm":None} ), 
        ("ADD S3, S1, X12", True, {"rs1":9, "rs2":12, "rd":19, "imm":None} ),
        ("ADD  S3   ,  S1  ,    X12", True, {"rs1":9, "rs2":12, "rd":19, "imm":None} ), 
        ("    ADD S3, S1, X12    ", True, {"rs1":9, "rs2":12, "rd":19, "imm":None} ),
        ("adds3s1s2", False, None ),
        ("  adds3s1s2  ", False, None )
        
])

def test_Instruction(input_inst, valid_inst, expected_operands):
    
    if not valid_inst:
        with pytest.raises(InstructionError):
            inst = Instruction(input_inst)
    else:
        inst = Instruction(input_inst)
        if expected_operands['rs1']:
            assert inst.rs1 == expected_operands['rs1']
        if expected_operands['rs2']:
            assert inst.rs2 == expected_operands['rs2']
        if expected_operands['rd']:
            assert inst.rd == expected_operands['rd']
        if expected_operands['imm']:
            assert inst.imm == expected_operands['imm']
