import re
from src.isa import REGISTER_FILE, INSTRUCTION_SET

class InstructionError(Exception):
  ...
# TODO:
# Add 'label' instance variable to replace 'imm' for Branch and Jump instructions
# - Update extract_operands to assign label to self.label instead of self.imm
class Instruction:
  '''
  Instruction object is exactly one line of assembly string (e.g add, s3, s2, s1)
  Validates instruction format, mnemonic, registers and immediate.

  Stores as instance variables:
  - Input instruction lower-cased and stripped of whitespace
  - Instruction mnemonic
  - Instruction Type
  - Control bits (Opcode, funct3/7 fields.)
  - Operands (destination/source registers, immediate)

  '''
  def __init__(self, instruction: str):
    self.instruction = self._parse_instruction(instruction)
    self.mnemonic = self._parse_mnemonic()
    self.type = self._parse_type()
    self._initialize_operands()
    self.extract_operands()

    self.op = INSTRUCTION_SET[self.type][self.mnemonic]["op"]
    self.funct3 = INSTRUCTION_SET[self.type][self.mnemonic]["funct3"]
    self.funct7 = INSTRUCTION_SET[self.type][self.mnemonic]["funct7"]
  
        
 
  
  def _parse_instruction(self, instruction: str) -> str:
    '''
    Initialize instruction by lowercasing and striping whitespace
    Basic format checking
    '''
    # instruction is not in format "mnemonic operands"
    if len( instruction.split(" ", 1)) != 2:
      raise InstructionError(f"Invalid instruction format:'{instruction}' \nExpected: 'mnemonic(e.g add)' + ' ' + 'operands(e.g s2, s1, s0)' ")

    return instruction.lower().strip()



  def _parse_mnemonic(self) -> str:
     '''
     Extract the mnemonic from instruction (e.g add)
     Validate mnemonic against instruction set
     '''
     # Mnemonic is the first set of characters in an assembly instruction, specifying the operation to perform on the given operands
     # There must be whitespace between the mnemonic and operands
     mnemonic = self.instruction.split(" ", 1)[0]
     
     # Check if mnemonic is in INSTRUCTION_SET look-up table
     for type in INSTRUCTION_SET.values():
      if mnemonic in type:
        return mnemonic
                   
        
     raise InstructionError(f"Invalid or unsupported instruction: '{mnemonic}' \nCheck documentation for all supported operations")  
        
        

  def _parse_type(self) -> str:
    '''
    Set instruction type (R/I/S/B/U/J) based on the mnemonic
    '''
    for type in INSTRUCTION_SET:
      if self.mnemonic in INSTRUCTION_SET[type]:
       # Useful for validating format since load instructions have a different format than the rest of the I-type instructions
       if self.mnemonic in ["lw", "lb", "lh"]: 
        self.load_type = True
       else:
        self.load_type = False

        return type
    # Should not reach here since mnemonic parser has validated the mnemonic  
    raise InstructionError(f"Instruction type undeterminable for mnemonic: {self.mnemonic}")

  

  def _initialize_operands(self):
    '''
    Sets all operand variables to None-type, extract_operands() sets the operands to their value from the instruction
    If operand is not in the instruction, the instance variable remains as None.
    '''
    self._rd = None
    self._rs1 = None
    self._rs2 = None
    self._imm = None
 
  @property
  def rs1(self):
    return self._rs1
  
  @rs1.setter
  def rs1(self, register: str):
    # Validate register
    if self.check_register(register):
      # Convert the register to its respective register number 
      # E.g 'zero' = 0 
      self._rs1 = REGISTER_FILE[f"{register}"]
    

  @property
  def rs2(self):
    return self._rs2
  
  @rs2.setter
  def rs2(self, register: str):
    # Validate register
    if self.check_register(register):
      # Convert the register to its respective register number 
      self._rs2 = REGISTER_FILE[f"{register}"]

  @property
  def rd(self):
    return self._rd
  
  @rd.setter
  def rd(self, register: str):
    # Validate register
    if self.check_register(register):
      # Convert the register to its respective register number 
      self._rd = REGISTER_FILE[f"{register}"]

  @property
  def imm(self):
    return self._imm
  
  @imm.setter
  def imm(self, immediate: str):
    # Convert immediate to decimal
    try:
      immediate_int = int(f"{immediate}", 0)
    except ValueError:
      raise InstructionError(f"Invalid immediate: '{immediate}'  \nImmediates must be either: \n -Decimal \n -Hexadecimal prefixed with '0x' \n -Binary prefixed with '0b'")
      

    if self.check_immediate(immediate_int):
      self._imm = immediate_int
    

  
  def extract_operands(self):
    '''
    Extract operands and assign them to instance variable e.g obj.rs1 = s0
    This also validates the operands themselves since they go through their setter

    Checks if operands are in the correct format according to instruction type
    e.g R-type instructions are in the format "mnemonic a, b, c"
    '''
 
    match self.type:

      case "R-type" | "B-type":
        
        # mnemonic space(req.), operand, operand, operand - whitespace next to operands ignored   
        if operands := re.match(r"^[a-z]+ +([a-z0-9]+) *, *([a-z0-9]+) *, *(-?[a-z0-9]+)$", self.instruction):

          if self.type == "R-type":
            # R-type : (mne) rd, rs1, rs2
            self.rd, self.rs1, self.rs2 = operands.groups()        
            
          if self.type == "B-type":
            # B-type : (mne) rs1, rs2, imm   imm = branch offset
            self.rs1, self.rs2, self.imm = operands.groups()

          return True
        
      case "I-type":

        # Load instructions are in the same format as S-type instructions
        if self.load_type:

          if operands := re.match(r"^[a-z]+ +([a-z0-9]+) *, *(-?[a-z0-9]+)\(([a-z0-9]+)\)$", self.instruction):
            # Load I-type : (mne) rd, imm(rs1)
            self.rd, self.imm, self.rs1,  = operands.groups()
            return True
        
        elif operands := re.match(r"^[a-z]+ +([a-z0-9]+) *, *([a-z0-9]+) *, *(-?[a-z0-9]+)$", self.instruction):
            # I-type : (mne) rd, rs1, imm
            self.rd, self.rs1, self.imm = operands.groups()
            return True
        
      case "S-type":

        # mnemonic space(req.), operand, operand(operand) - whitespace next to operands ignored
        if operands := re.match(r"^[a-z]+ +([a-z0-9]+) *, *(-?[a-z0-9]+)\(([a-z0-9]+)\)$", self.instruction):
          # S-type : (mne) rs2, imm(rs1)   imm = offset
          self.rs2, self.imm, self.rs1 = operands.groups()
          return True

      case "U-type" | "J-type":

        # mnemonic space(req.), operand, operand - whitespace next to operands ignored
        if operands  := re.match(r"^[a-z]+ +([a-z0-9]+) *, *(-?[a-z0-9]+)$", self.instruction):
          # U/J-type : (mne) rd, label
          self.rd, self.imm = operands.groups()
          return True
        
    raise InstructionError(f"Invalid format for '{self.type}' instruction: '{self.instruction}'\n" f"Expected format: '{self.valid_format()}' ") 
          
     
  def valid_format(self):
    match self.type:
      case "R-type":
        return "(mnemonic) rd, rs1, rs2"
      
      case "I-type":
        if self.load_type:
          return "(mnemonic) rs2, offset(rs1)"
        else:
          return "(mnemonic) rd, rs1, immediate"
      
      case "S-type":
        return "(mnemonic) rs2, offset(rs1)"
      
      case "B-type":
        return "(mnemonic) rs1, rs2, label"
      
      case "U-type":
        return "(mnemonic) rd, immediate"
      
      case "J-type":
        return "(mnemonic) rd, label"


  def check_register(self, register: str) -> bool:

        if register in REGISTER_FILE:
          return True
        else:
          raise InstructionError(f"Invalid register: '{register}'")
        
  def check_immediate(self, immediate: int) -> bool:
          '''
          Checks if immediate value is valid

          I/S-type should be <= 12-bit 
            - I-type shifts should be <= 5-bit since shifting more than 32 bits is redundant (32-bit register size)
          B-type should be <= 13-bit
          U-type should be <= 20-bit 
          J-type should be <= 21-bit
          '''
          shift_instructions = ["slli", "srli", "srai"]
            

          match self.type:
            case "I-type" | "S-type":
              
              # If instruction is shift 
              if self.mnemonic in shift_instructions:
                # Shift instructions immediate is 5-bits since shifting more than 32-bits is redundant (32-bit registers)
                # Immediate is unsigned - cannot shift by negative amount.
                # Add one since range upper limit is exclusive
                valid_range = range(0, (2**5)+1)
              else:
                # Immediate is a 12-bit signed number (two's complement) 
                # Signed numbers are in the range: -2^n to 2^n - 1  where n is number of bits
                # Since upper limit of range is exclusive, subtracting one is not neccesary
                valid_range = range(-(2**12), 2**12)
              
              if immediate in valid_range:
                return True
              
            case "B-type":
              # Immediate is the branch offset - number of bytes to the label
              # The immediate is 13-bit signed number
              valid_range = range(-(2**13), 2**13)
              if immediate in valid_range:
                return True
              
            case "U-type":
              # Immediate is a 20-bit signed number
              valid_range = range(-(2**20), 2**20)
              if immediate in valid_range:
                return True
              
            case "J-type":
              # Immediate is the jump offset - number of bytes to the label
              # Immediate is 21-bit 
              valid_range = range(-(2**21), 2**21)
              if immediate in valid_range:
                return True

          raise InstructionError(f"Immediate: '{immediate}' out of range \n'{self.type}' instruction immediate must be in the range: {valid_range[0]} - {valid_range[-1]}")

  

        
      