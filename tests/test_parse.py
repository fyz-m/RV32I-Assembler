from src.parse import first_pass,second_pass, symbol_table, get_offset
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
first_pass_output_1 = """\
0x0: addi t0, t0, 10
0x4: addi s2, s2, 1
0x8: bne s2, t0, label
0xc: lw s7, 12(s2)
"""
second_pass_output_1 = '''\
00a28293
00190913
00591263
00c92b83
'''  
table1 = {"label": 0xc}

test2 = """\
# s0 = button, s1 = amt
case1:
  addi t0, zero, 1 # t0 = 1
  bne s0, t0, case2 # button = = 1?
  addi s1, zero, 20 # if yes, amt = 20
  jal x0, done # break out of case
case2:
  addi t0, zero, 2 # t0 = 2
  bne s0, t0, case3 # button = = 2?
  addi s1, zero, 50 # if yes, amt = 50
  jal x0, done # break out of case
case3:
  addi t0, zero, 3 # t0 = 3
  bne s0, t0, default # button = = 3?
  addi s1, zero, 100 # if yes, amt = 100
  jal x0, done # break out of case
default:
  add s1, zero, zero # amt=0
done:
  addi zero, zero, 0
"""
first_pass_output_2 = """\
0x0: addi t0, zero, 1 # t0 = 1
0x4: bne s0, t0, case2 # button = = 1?
0x8: addi s1, zero, 20 # if yes, amt = 20
0xc: jal x0, done # break out of case
0x10: addi t0, zero, 2 # t0 = 2
0x14: bne s0, t0, case3 # button = = 2?
0x18: addi s1, zero, 50 # if yes, amt = 50
0x1c: jal x0, done # break out of case
0x20: addi t0, zero, 3 # t0 = 3
0x24: bne s0, t0, default # button = = 3?
0x28: addi s1, zero, 100 # if yes, amt = 100
0x2c: jal x0, done # break out of case
0x30: add s1, zero, zero # amt=0
0x34: addi zero, zero, 0
"""
second_pass_output_2 = '''\
00100293
00541663
01400493
0280006f
00200293
00541663
03200493
0180006f
00300293
00541663
06400493
0080006f
000004b3
00000013
'''
table2= {"done": 0x34, "case1": 0x0, "case2": 0x10, "case3": 0x20, "default": 0x30}

@pytest.mark.parametrize("test_input, fp_output_expected, expected_symbol_table, sp_output_expected", [
    (test1, first_pass_output_1, table1, second_pass_output_1),
    (test2, first_pass_output_2, table2, second_pass_output_2),
    
])
  

def test_passes(tmp_path, test_input, fp_output_expected, expected_symbol_table, sp_output_expected):
      
      input_file = tmp_path / "test.txt"
      input_file.write_text(test_input)

      fp_output_file = tmp_path / "fp_output.txt"
      first_pass(input_file, fp_output_file)
      
      assert symbol_table == expected_symbol_table
      assert fp_output_file.read_text() == fp_output_expected
      

      sp_output_file = tmp_path / "sp_output.txt"
      second_pass(fp_output_file, sp_output_file)    

      assert sp_output_file.read_text() == sp_output_expected
      symbol_table.clear()
      





