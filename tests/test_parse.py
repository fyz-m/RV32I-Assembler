from src.parse import first_pass, symbol_table, get_offset
import pytest


@pytest.mark.parametrize("label, label_address, current_address, expected_offset", [
    ("jump", 0x20, 0x12, 0xE),
    ("jump", 40, 100, -60),
    
])

def test_offset(label, label_address, current_address, expected_offset):
      symbol_table[label] = label_address
      assert get_offset(label, current_address) == expected_offset 
      del symbol_table[label]
      




test1 = """\
# test
addi t0, t0, 10
# comment
# beq s2, t0, loop
addi s2, s2, 1
bne s2, t0, label
# label:
              
label: 
               
lw s7, 12(s2)
"""
output1 = """\
0x0: addi t0, t0, 10
0x4: addi s2, s2, 1
0x8: bne s2, t0, label
0xc: lw s7, 12(s2)
"""

table1 = {"label": "0xc"}

test2 = """\
# s0 = button, s1 = amt
case1:
  addi t0, zero, 1 # t0 = 1
  bne s0, t0, case2 # button = = 1?
  addi s1, zero, 20 # if yes, amt = 20
  j done # break out of case
case2:
  addi t0, zero, 2 # t0 = 2
  bne s0, t0, case3 # button = = 2?
  addi s1, zero, 50 # if yes, amt = 50
  j done # break out of case
case3:
  addi t0, zero, 3 # t0 = 3
  bne s0, t0, default # button = = 3?
  addi s1, zero, 100 # if yes, amt = 100
  j done # break out of case
default:
  add s1, zero, zero # amt=0
done:
  jal ra, function
"""
output2 = """\
0x0: addi t0, zero, 1 # t0 = 1
0x4: bne s0, t0, case2 # button = = 1?
0x8: addi s1, zero, 20 # if yes, amt = 20
0xc: j done # break out of case
0x12: addi t0, zero, 2 # t0 = 2
0x14: bne s0, t0, case3 # button = = 2?
0x18: addi s1, zero, 50 # if yes, amt = 50
0x1c: j done # break out of case
0x20: addi t0, zero, 3 # t0 = 3
0x24: bne s0, t0, default # button = = 3?
0x28: addi s1, zero, 100 # if yes, amt = 100
0x2c: j done # break out of case
0x30: add s1, zero, zero # amt=0
0x34: jal ra, function
"""

table2= {"done": "0x34", "case1": "0x0", "case2": "0x12", "case3": "0x20", "default": "0x30"}

@pytest.mark.parametrize("test_input, expected_output, expected_symbol_table", [
    (test1, output1, table1),
    (test2, output2, table2),
    
])
  

def test_first_pass(tmp_path, test_input, expected_output, expected_symbol_table):
      input_file = tmp_path / "test.txt"
      input_file.write_text(test_input)

      output_file = tmp_path / "output.txt"

      
      first_pass(input_file, output_file)
      
      assert symbol_table == expected_symbol_table
      assert output_file.read_text() == expected_output
      

