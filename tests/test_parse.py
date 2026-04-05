from src.parse import first_pass, symbol_table


test_lines = [
    "# test",
    "addi t0, t0, 10",
    "# comment",
    "# beq s2, t0, loop",
    "addi s2, s2, 1",
    "bne s2 t0, abc",
    "# abc:",
    "              ",
    "abc: ",
    "               ",
    "lw s7, 12(s2)",
]

def test_first_pass(tmp_path):
    input_file = tmp_path / "test.txt"
    with open(f"{input_file}", "w") as f:
      for line in test_lines:
        f.write(f"{line}\n")


    output_file = tmp_path / "output.txt"
    first_pass(input_file, output_file)
    
    with open(f"{output_file}", "r") as f:
      actual_lines = f.readlines()
    
      expected_lines = [
        ("0x4: addi t0, t0, 10\n"),
        ("0x8: addi s2, s2, 1\n"),
        ("0xc: bne s2 t0, abc\n"),
        ("0x10: lw s7, 12(s2)\n"), 
    ]

      assert actual_lines == expected_lines
      assert symbol_table == {"abc":0x10}
