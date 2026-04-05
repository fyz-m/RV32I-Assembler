from src.parse import first_pass, symbol_table


test_input = """\
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
expected_output = """\
0x4: addi t0, t0, 10
0x8: addi s2, s2, 1
0xc: bne s2, t0, label
0x10: lw s7, 12(s2)
"""

expected_symbol_table = {"label": "0x10"}

def test_first_pass(tmp_path):
    input_file = tmp_path / "test.txt"
    input_file.write_text(test_input)

    output_file = tmp_path / "output.txt"
    first_pass(input_file, output_file)

    assert output_file.read_text() == expected_output
    assert symbol_table == expected_symbol_table
