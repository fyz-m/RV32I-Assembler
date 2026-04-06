''' 
First parse: 
- Remove blank lines and comments

- Add memory address to each instruction 
- Collect labels for encoding in a symbol table 
- Use regex to find labels and to seperate them from instructions


Second parse:
Assign each line as an instruction object - validation and operand extracting
Encode

'''
import re
from src.Instruction import Instruction
from src.encode import encode


# Contains the label and its instruction address
symbol_table = {}


def first_pass(input_file, output_file):
  '''
  Adds memory address to each instruction, collects labels in a symbol table
  '''
  lines_to_write = []
  address = 0

  with open(f"{input_file}", "r") as f:
    lines = f.readlines()
    line_num = 0

    for line in lines:
       line = line.strip() 
       # Skip if line is a comment or blank
       if is_comment(line) or not line:
          continue    
       # Address of first instruction remains 0    
       if line_num != 0:
         address += 4

       line_num += 1
       instruction = line

       if label := collect_label(line):
            instruction = line.replace(f"{label}:", "")

            if label in symbol_table:
               raise ValueError(f"Line {line_num}: \nLabel: '{label}' already used")
            
            # If instruction is not on the same line as label, skip to the next line e.g:
            #  
            # beq s2, 0, label  ------->   0x0: beq s2, 0, label (label converted into branch offset in second pass, which is 8-bytes here)
            # addi s2, s2, -1              0x4: addi s2, s2, -1 
            # label:                       0x8: xor s2, s1, s0
            # (blank/comment lines)
            # xor s2, s1, s0
            if not instruction:
               # As above, the address where the label is located == address of instruction label is pointing to 
               symbol_table[label] = address
               # This gives the address of the current label to the next instruction line, since address += 4 on the next non blank/comment line
               address -= 4
               continue
            
            else:
              symbol_table[label] = address
          
       lines_to_write.append(f"{hex(address)}: {instruction}\n")


  with open(f"{output_file}", "w") as output:
     output.writelines(lines_to_write)
   
           

def second_pass(input_file, output_file):
    
    encoded_instructions = []
    
    with open(f"{input_file}", "r") as f:
      lines = f.readlines()
      line_num = 0

      for line in lines:
         if match := re.match(r"^(.*):(.+)( *#.*)?$", line):
            address = int(match.group(1), 0)
            instruction = Instruction(match.group(2))

            if instruction.label is not None:
               instruction.imm = get_offset(instruction.label, address) # type: ignore

            encoded_inst = format(encode(instruction),'08x' )
            encoded_instructions.append(f"{encoded_inst}\n")

    with open(f"{output_file}", "w") as output:
     output.writelines(encoded_instructions)
    ...
          
def collect_label(line):

   if match := re.match(r"(.+):(.*)", line):
      return match.group(1).strip()
   else:
       return None


def is_comment(line: str) -> bool:
   
   if match := re.match(r"#.*", line):
      return True
   else:
      return False
   
def get_offset(label: str, current_address: int) -> int:
      '''
      Args
         Instruction object
         Address of the instruction
      
      Returns
         Branch/Jump offset 

      Example:
         4: LABEL 1:  offset =
         8: 
         12:
      A  16: beq x, x, LABEL 1/2
         20:
         24: LABEL 2: offset = 

         The address of the label is the branch target address
         The branch offset is the number of bytes from the branch instruction to the specified label

         For LABEL 1, branch offset is 24-16 = 8 bytes. BO = BTA - A
         For LABEL 2, branch offset is 4-16 = -12 bytes. BO = BTA - A 
      '''
      target_address = symbol_table[label]

      return target_address - current_address


      

