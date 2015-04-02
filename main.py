from Chem import *

if __name__ == "__main__":
   Na = Elements["Na"]
   O = Elements["O"]
   H = Elements["H"]
   OH = Molecule(O, H)
   NaOH2 = Molecule(Na, O, H, O, H)
   H2O = Molecule(H, H, O)
   
   eq = Reagent(NaOH2) + Reagent(H2O) == Product(Cation(Na)) + Product(Anion(OH)) + Product(H2O)
   