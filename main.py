from Chem import *

if __name__ == "__main__":
   C = Elements["C"]
   O = Elements["O"]
   CO = Molecule(C, O)
   
   eq = Reagent(CO) == Product(Molecule(C)) + Product(Molecule(O, O))

   print(eq)
   