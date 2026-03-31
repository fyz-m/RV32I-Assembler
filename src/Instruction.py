import re
from src.isa import REGISTER_FILE, INSTRUCTION_SET
class Instruction:
  '''
  Instruction object is exactly one line of assembly string (e.g add, s3, s2, s1)
  Validates instruction format, mnemonic, registers and immediate where applicable.
  '''
  def __init__(self, instruction):
    self.Instruction = instruction
    self.Mnemonic = None
    self.Type = None
    self.Operands = None
    self.Registers = None
    
    
    
  @property
  def Instruction(self):
      return self._Instruction
  
  @Instruction.setter
  def Instruction(self, instruction):
    '''
    Initialize instruction by lowercasing and striping whitespace
    Basic format checking
    '''
    # instruction is not in format "mnemonic operands"
    if len( instruction.split(" ", 1)) != 2:
      raise ValueError(f"Invalid instruction format:'{instruction}' \nExpected: 'mnemonic(e.g add)' + ' ' + 'operands(e.g s2, s1, s0)' ")

    self._Instruction = instruction.lower().strip()


  @property
  def Mnemonic(self):
    return self._Mnemonic
  
  @Mnemonic.setter
  def Mnemonic(self, _=None):
     '''
     Extract the mnemonic from instruction (e.g add)
     Check if mnemonic is a valid/supported operation i.e is in the instruction symbol table
     '''
     # Mnemonic is the first set of characters in an assembly instruction, specifying the operation to perform on the given operands
     # There must be whitespace between the mnemonic and operands
     mnemonic = self.Instruction.split(" ", 1)[0]
     
     # Check if mnemonic is in INSTRUCTION_SET look-up table
     for type in INSTRUCTION_SET.values():
      if mnemonic in type:
        self._Mnemonic = mnemonic
        return           
        
     raise ValueError(f"Invalid or unsupported instruction: '{mnemonic}' \n Check documentation for all supported operations")  
        
     
     
  @property
  def Type(self):
    return self._Type
  @Type.setter
  def Type(self, _=None):
    '''
    Set instruction type based on the mnemonic
    E.g "add" sets type to "R-type" 
    '''
    for type in INSTRUCTION_SET:
      if self.Mnemonic in INSTRUCTION_SET[type]:
        self._Type = type
    

  @property
  def Operands(self, _=None):
    return self._Operands
  
  @Operands.setter
  def Operands(self, _):
    '''
    Returns the list of operands in an instruction without whitespace and in lowercase
    '''
    # Instruction without mnemonic (contains operands)
    inst_half = self.Instruction.split(" ", 1)[1]

    # Split into individual operands
    # Operands are seperated by commas in assembly, e.g s1, s2, s3
    operand_list = inst_half.split(",")       

    # Strip whitespace and lowercase  operands
    operands = [operand.lower() and operand.strip() for operand in operand_list] 
    self._Operands = operands


    
  
  def extract_operands(self):
    '''
    Checks if operands are in the correct format according to instruction type
    e.g R-type instructions are in the format "mnemonic rd, rs1, rs2"
    Extract operands
    '''

    match self.Type:

      case "R-type" | "I-type" | "B-type":
        
        # mnemonic space(req.), operand, operand, operand - whitespace next to operands ignored   
        if operands := re.match(r"^[a-z]+ +([a-z0-9]+) *, *([a-z0-9]+) *, *([a-z0-9]+)$", self.Instruction):
          if self.Type == "R-type":
            #R-type : (mne) rd, rs1, rs2
            self.rd, self.rs1, self.rs2 = operands.groups()
          if self.Type == "I-type":
            #I-type : (mne) rd, rs1, imm
            self.rd, self.rs1, self.imm = operands.groups()
          if self.Type == "B-type":
            #B-type : (mne) rs1, rs2, imm   imm = branch offset
            self.rs1, self.rs, self.imm = operands.groups()

          return True
        
      case "S-type":

        # mnemonic space(req.), operand, operand(operand) - whitespace next to operands ignored
        if operands := re.match(r"^[a-z]+ +([a-z0-9]+) *, *([a-z0-9]+)\(([a-z0-9]+)\)$", self.Instruction):
          #S-type : (mne) rs2, imm(rs1)   imm = offset
          self.rs2, self.imm, self.rs1 = operands.groups()
          return True

      case "U-type" | "J-type":

        # mnemonic space(req.), operand, operand - whitespace next to operands ignored
        if operands  := re.match(r"^[a-z]+ +([a-z0-9]+) *, *([a-z0-9]+)$", self.Instruction):
          self.rd, self.imm = operands.groups()
          return True
        
    raise ValueError(f"Invalid format for instruction type '{self.Type}': '{self.Instruction}'\nShould be in format: '{self.Valid_format}'") 
          
     

  def checkReg(self, register):

        if register in REGISTER_FILE:
          return True
        else:
          raise ValueError(f"Invalid register: '{register}'")
        
  def checkImm(self, immediate):
          '''
          Checks if immediate value is valid

          I/S-type should be <= 12-bit 
            - I-type shifts should be <= 5-bit since shifting more than 32 bits is redundant (32-bit register size)
          B-type shoulbe be <= 13-bit
          U-type should be <= 20-bit 
          J-type should be <= 21-bit
          '''
          shift_instructions = ["slli", "srli", "srai"]

  
          # Shift instructions immediate is 5-bits since shifting more than 32-bits is redundant (32-bit registers)
          # Immediate is unsigned - cannot shift by negative amount.
          # Add one since range upper limit is exclusive
          valid_range = range(0, (2*5)+1)

          if self.Mnemonic in shift_instructions:
            if immediate in valid_range:
              return True
            

          match self.Type:
            case "I-type" | "S-type":
              # Immediate is a 12-bit signed number (two's complement) 
              # Signed numbers are in the range: -2^n to 2^n - 1  where n is number of bits
              # Since upper limit of range is exclusive, subtracting one is not neccesary
              valid_range = range(-(2*12), 2*12)
              if immediate in valid_range:
                return True
              
            case "B-type":
              # Immediate is the branch offset - number of bytes to the label
              # The immediate is 13-bit signed number
              valid_range = range(-(2*13), 2*13)
              if immediate in valid_range:
                return True
              
            case "U-type":
              # Immediate is a 20-bit signed number
              valid_range = range(-(2*20), 2*20)
              if immediate in valid_range:
                return True
              
            case "J-type":
              # Immediate is the jump offset - number of bytes to the label
              # Immediate is 21-bit 
              valid_range = range(-(2*21), 2*21)
              if immediate in valid_range:
                return True

          raise ValueError(f"Immediate: '{immediate}' out of range \n'{self.Type}' instruction immediate must be in the range: {valid_range}")

  
  def Valid_format(self):
    match self.Type:
      case "R-type":
        return "(mnemonic) rd, rs1, rs2"
      case "I-type":
        return "(mnemonic) rd, rs1, imm"
      case "S-type":
        return "(mnemonic) rs2, imm(rs1)"
      case "B-type":
        return "(mnemonic) rs1, rs2, label"
      case "U-type" | "J-type":
        return "(mnemonic) rd, imm"


  
  @property
  def Registers(self):
    return self._Registers
  @Registers.setter
  def Registers(self, _=None):
    '''
    Converts registers into their corresponding number after validation
    '''
  
    match self.Type:
      case "R-type":
        rs1 = self.Operands[1]
        rs2 = self.Operands[2]
        rd = self.Operands[0]

      case "I-type":
        rs1 = self.Operands[1]
        rs2 = None
        rd = self.Operands[0]
        
      case "S-type":
        rs1 = re.search(r"\((.*)\)", self.Operands[1] ).group(1)
        rs2 = self.Operands[0]
        rd = None

      case "B-type":
        rs1 = self.Operands[0]
        rs2 = self.Operands[1]
        rd = None

      case "U-type":
        rs1 = None
        rs2 = None
        rd = self.Operands[0]

      case "J-type":
        rs1 = None
        rs2 = None
        rd = self.Operands[0]
    

    RegDict = {}
    if rs1:
      RegDict["rs1"] = REGISTER_FILE[rs1]
    if rs2:
      RegDict["rs2"] = REGISTER_FILE[rs2]
    if rd:
      RegDict["rd"] = REGISTER_FILE[rd]
    
    self._Registers = RegDict
      
    
  
  

        
      