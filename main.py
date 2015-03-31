from Chem import *

if __name__ == "__main__":
   C = Elements["C"]
   O = Elements["O"]
   CO = Molecule(C, O)
   
   eq = Reagent(CO) == Product(C) + Product(Molecule(O, O))
   
   print(eq)

   s = Sieve(eq.balance(), 100, Grams(CO, 20))
   
   print(s)
   
   s += Grams(CO, 70)
   
   print(s)
   
   print(s[C])
   print(s[CO])
