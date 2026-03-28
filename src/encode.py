
'''
Encode instruction according to instruction type: R, I, S/B, U/J
Registers must already be converted to their number (defined by RISC-V ISA)
input instruction example format:
  "add 18, 19, 20" 

'''
import re

class Instruction:
  def __init__(self, instruction):
    self.instruction = instruction
    self.Mnemonic = instruction
    self.Type = instruction
    self.Operands = instruction
    self.Registers = instruction

  @property
  def Mnemonic(self):
    return self._Mnemonic
  
  @Mnemonic.setter
  def Mnemonic(self, instruction):
     
     if mnemonic := instruction.split(" ", 1)[0]:
      for type in Instructions:
        if mnemonic in Instructions[type]:
          self._Mnemonic = mnemonic
          return None          
        else:
          pass
        
      raise ValueError(f"Invalid instruction: '{mnemonic}'")  
        
     else:
      raise ValueError(f"Invalid instruction: '{instruction}'")
     
  @property
  def Type(self):
    return self._Type
  @Type.setter
  def Type(self):

    for type in Instructions:
      if self.Mnemonic in Instructions[type]:
        self._Type = type 


  @property
  def Operands(self):
    return self._Operands
  @Operands.setter
  def Operands(self):
    if inst_half := self.instruction.split(" ", 1)[1]: #Instruction without mnemonic (contains operands)
      operands = inst_half.split(",")            #Split into individual operands
      if self.checkOperands(operands):
        self._Operands = operands
    else:
      raise ValueError
    
  
  def checkOperands(cls, operands):
    '''
    checks if operands are in the correct format according to instruction type
    Does not check if operands are correct.
    '''


  
  @property
  def Registers(self):
    return self._Registers
  @Registers.setter
  def Registers(self):
    #R-type : (mne) rd, rs1, rs2
    #I-type : (mne) rd, rs1, imm
    #S-type : (mne) rs2, imm(rs1)   imm = offset
    #B-type : (mne) rs1, rs2, imm   imm = branch offset
    #U-type : (mne) rd, imm
    #J-type : (mne) rd, imm
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
        rs1 = re.search(r".+(.+)", self.Operands[2]).groups(1)
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
    
    if self.checkReg(rs1, rs2, rd):
      self._Registers = {
        "rs1": rs1,
        "rs2": rs2,
        "rd": rd
      } 

    def checkReg(*Registers):
      for register in Registers:
        if register not in Registers:
          return False
        
      return True

Registers = {
   "zero":0, "x0":0,
   "ra":1, "x1":1,
   "sp":2, "x2":2,
   "gp":3, "x3":3,
   "tp":4, "x4":4,
   "t0":5, "x5":5,
   "t1":6, "x6":6,
   "t2":7, "x7":7,
   "s0":8, "x8":8, "fp":8,
   "s1":9, "x9":9,
   "a0":10, "x10":10,
   "a1":11, "x11":11,
   "a2":12, "x12":12,
   "a3":13, "x13":13,
   "a4":14, "x14":14,
   "a5":15, "x15":15,
   "a6":16, "x16":16,
   "a7":17, "x17":17,
   "s2":18, "x18":18,
   "s3":19, "x19":19,
   "s4":20, "x20":20,
   "s5":21, "x21":21,
   "s6":22, "x22":22,
   "s7":23, "x23":23,
   "s8":24, "x24":24,
   "s9":25, "x25":25,
   "s10":26, "x26":26,
   "s11":27, "x27":27,
   "t3":28, "x28":28,
   "t4":29, "x29":29,
   "t5":30, "x30":30,
   "t6":31, "x31":31,
}

Instructions = {
  "R-type": {
    "add": {"controlBits": (51, 0, 0)},  # Controlbits = opcode, func3, func7 
    "sub": {"controlBits": (51, 0, 32)},
    "sll": {"controlBits": (51, 1, 0)},
    "slt": {"controlBits": (51, 2, 0)},
    "sltu": {"controlBits": (51, 3, 0)},
    "xor": {"controlBits": (51, 4, 0)},
    "srl": {"controlBits": (51, 5, 0)},
    "sra": {"controlBits": (51, 5, 32)}
  },

  "I-type": {
    "addi": {"controlBits": (19, 0, None)},
  },

  "S-type": {
    "sw":{"controlBits": (35, 2, None) },
  },

  "B-type": {
    "beq":{"controlBits": (99, 0, None) },
  },

  "U-type": {
   "lui": {"controlBits": (55, None, None) },
  },

  "J-type": {
    "jal":{"controlBits": (111, None, None) },
  }
}



def encode(instruction):

  Type = getType(instruction)
  fields = getFields(Type, instruction)

  match Type:
    case "R-type":
      encode_R_type(instruction)
    case "I-type":
      encode_I_type(instruction)
    case "S-type":
      encode_S_type(instruction)
    case "B-type":
      encode_B_type(instruction)
    case "U-type":
      encode_U_type(instruction)
    case "B-type":
      encode_B_type(instruction)


  
def getFields(type, instruction):
  '''
  Returns the field values of each instruction
  '''
  opcode, func3, func7 = Instructions[type][getMnemonic(instruction)]["controlBits"]
  


def encode_R_type(opcode, rd, rs1, rs2, func3, func7):
  ...

def encode_I_type(opcode, rd, rs1, func3, imm):
  ...

def encode_S_type(opcode, rs1, rs2, func3, imm):
  ... 

def encode_B_type(opcode, rs1, rs2, func3, imm):
  ... 

def encode_U_type(opcode, rd, imm):
  ... 

def encode_J_type(opcode, rd, imm):
  ... 
