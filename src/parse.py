import re, os
from src.Instruction import Instruction, InstructionError
from src.encode import encode

# Contains labels and its instruction address
symbol_table = {}
error_list = []

def assemble(assembly_file, binary):
   '''
   Takes an assembly file as input and translates it into machine code
   '''
   # determime extension
   if binary:
      ext = "bin"
   else:
      ext = "txt"

   first_pass(assembly_file, "temp.txt")

   # Get name of input file
   assembly_file_name = assembly_file.split(".")[0]
   output_file_name = f"{assembly_file_name}_assembled.{ext}"

   second_pass("temp.txt", output_file_name, binary)

   os.remove("temp.txt")
   

   # Print error list
   if len(error_list) != 0:
      print(f"\n  Failed with {len(error_list)} error(s):\n")
      for error in sorted(error_list, key=lambda x: int(x.split(":")[0][10:])):
         print(error)
   else:
      print("Assembled successfully!")


def first_pass(input_file, output_file):
  '''
  Adds memory address to each instruction 
  Collects labels in a symbol table for offset/immediate calculation of J/B-type instructions
  Removes blank lines and comments
  '''
  lines_to_write = []
  # Address of first instruction remains 0    
  address = -4

  with open(f"{input_file}", "r") as f:
    lines = f.readlines()
    line_num = 0

    for line in lines:
       line_num += 1
       line = line.strip() 
       # Skip if line is a comment or blank
       if is_comment(line) or not line:
          continue    
       
       # Address increments by 4 since RISC-V is byte-addressable 
       address += 4
       instruction = line

       if label := collect_label(line):
            instruction = line.replace(f"{label}:", "")

            if label in symbol_table:
               
               error_list.append(
                  f"      line {line_num}: Label '{label}' already used \n"
                  f"       > {line}\n"
                  )
            
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
          
       lines_to_write.append(f"{line_num} {hex(address)}: {instruction}\n")


  with open(f"{output_file}", "w") as output:
     output.writelines(lines_to_write)
   
           

def second_pass(input_file, output_file, binary):
    '''
    Translates each instruction into machine code (hexadecimal)
    Removes comments beside instructions
    '''
   
    encoded_instructions = []
    
    with open(f"{input_file}", "r") as f:
      lines = f.readlines()
      
      for line in lines:
         
         if match := re.match(r"^([0-9]+) (.*): ([^#]+)(#.*)?$", line):
            line_num = match.group(1)
            address = int(match.group(2), 0)

            try:
               # Cancel pass if 10 errors are encountered 
               if len(error_list) >= 10:
                      return
               
               instruction = Instruction(match.group(3))
               if instruction.label is not None:
                  instruction.imm = get_offset(instruction.label, address) # type: ignore

               # Encode instruction
               if binary:
                  # Write as binary data
                  encoded_inst = encode(instruction).to_bytes(4, byteorder='little', signed=False) #type: ignore  
                  encoded_instructions.append(encoded_inst)
               else:
                  # Write as hexadecimal 
                  encoded_inst = f"{encode(instruction):08x}"
                  encoded_instructions.append(f"{encoded_inst}\n")

            except InstructionError as e:
                   error_list.append(f"      line {line_num}: {str(e)}\n")      
                   continue
            except KeyError:
                   error_list.append(
                                    f"      line {line_num}: Label '{instruction.label}' is referenced but was not found\n"
                                    f"       > {instruction.instruction}\n"
                                    )
                   continue

        
    if len(error_list) == 0:

      if binary:
         with open(f"{output_file}", "wb") as output:
            ebreak = 0x00100073.to_bytes(4, byteorder='little', signed=False)
            encoded_instructions.append(ebreak)

            output.writelines(encoded_instructions)
      else:
         with open(f"{output_file}", "w") as output:
            output.writelines(encoded_instructions)
      
          
def collect_label(line):
   '''
   Returns a label from a line if found

   E.g
      Loop: addi t0, t0, 1
   Returns:
      "Loop"
   '''
   if match := re.match(r"^([^#]+):(.*)$", line):
      return match.group(1).strip()
   else:
       return None


def is_comment(line: str) -> bool:
   '''
   Returns true if line is a comment and false if it is not
   '''
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


      
