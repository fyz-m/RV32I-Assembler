import argparse
from src.parse import assemble

def main():

  file, binary = get_arguments()
  assemble(file, binary)

  
def get_arguments():
  ...
  #Get input file to be converted and CLI arguments to output in binary or hex
  parser = argparse.ArgumentParser()

  parser.add_argument("-f", "--file", help="Assembly file to be converted into machine code")
  parser.add_argument("-b", "--binary", help="Output assembled file in binary (default: hexadecimal)",  action="store_true")

  args = parser.parse_args()
  
  return args.file, args.binary



if __name__ == "__main__":
  main()