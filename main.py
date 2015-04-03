from Chem import *

if __name__ == "__main__":
   Na = Elements["Na"]
   O = Elements["O"]
   H = Elements["H"]
   OH = Molecule(O, H)
   NaOH2 = Molecule(Na, O, H, O, H)
   
   eq = Reagent(NaOH2) == Product(Cation(Na)) + Product(Anion(OH))
   
   # 0,010 M = n/V => 0,010 M = n / 11,1 ml => 0,010 M * 11,1 ml
   s = Sieve(eq.balance(), 5, Moles(Anion(OH), 0.010 * 11.1 * 10**-3))
   