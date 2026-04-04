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

Symbol_table = {}

def main():
   first_pass("test.txt")
   print(Symbol_table)

def first_pass(file):
  lines_to_write = []
  address = 0

  with open(f"{file}", "r") as f:
    lines = f.readlines()
    line_num = 0
    for line in lines:
       line = line.strip() 
       if is_comment(line) or not line:
          pass    
       
       else:
          line_num += 1
          address += 4

          if match := re.match(r"(.+):(.*)", line):
            label = match.group(1).strip()
            line = match.group(2).strip()

            if label in Symbol_table:
               raise ValueError(f"Line {line_num}: \nLabel: '{label}' already used")
            # If instruction is not on the same line as label, skip to the next line
            if not line:
               # Label gets address of next non-empty line
               Symbol_table[label] = hex(address+4)
               continue
            
            else:
              Symbol_table[label] = hex(address)
          
          lines_to_write.append(f"{hex(address)}: {line}\n")


  with open(f"output.txt", "w") as output:
     output.writelines(lines_to_write)
   
           
            

   

def is_comment(line):
   
   if match := re.match(r"#.*", line):
      return True
   else:
      return False
   
main()