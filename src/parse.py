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
            # If instruction is not on the same line as label, skip to the next line
            # e.g loop:
            #
            # addi s2,s1,s0
            if not instruction:
               # Label gets address of next instruction line 
               # Blank lines do not increment the address so next address will always be the instruction the label is pointing to
               symbol_table[label] = hex(address+4)
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
   
