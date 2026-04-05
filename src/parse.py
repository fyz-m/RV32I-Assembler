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
# Contains the label and its instruction address
symbol_table = {}

'''def main():
   first_pass("test.txt", "temp.txt")
   print(Symbol_table)'''

def first_pass(input_file, output_file):
  '''
  Adds memory address to each instruction, collects labels in a symbol tabel
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
           
       line_num += 1
       address += 4
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
               symbol_table[label] = hex(address)
               # This gives the address of the current label to the next instruction line, since address += 4 on the next non blank/comment line
               address -= 4
               continue
            
            else:
              symbol_table[label] = hex(address)
          
       lines_to_write.append(f"{hex(address)}: {instruction}\n")


  with open(f"{output_file}", "w") as output:
     output.writelines(lines_to_write)
   
           
            
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
   
