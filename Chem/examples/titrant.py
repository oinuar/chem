from Chem import *

Mg = Elements["Mg"]
O = Elements["O"]
H = Elements["H"]
Cl = Elements["Cl"]

OH = Molecule(O, H) # base
MgOH2 = Molecule(Mg, O, H, O, H) # alkine earth metal, in this case, magnesium
HCl = Molecule(H, Cl) # titrant, a strong acid

# 0.010 M = n / 11.1 ml => 0.010 M * 11.1 ml * 10 ** -3
cHCl = Concentration(11.1 * 10**-3, Moles(HCl, 0.010 * 11.1 * 10**-3))

# Chemical reaction in water
eq = Reagent(MgOH2) == Product(Cation(Mg)) + Product(Anion(OH))

# HCl is a strong acid so it dissolves completely in water and removes all OH-.
s = Sieve(eq.balance(), 5 * 10**-3, cHCl.content.to(Anion(OH)))

# Get the concentrations of ions in solution.
cMg = s[Cation(Mg)]
cOH = s[Anion(OH)]

print(cMg)
print(cOH)
print("Ks = [Mg+][OH-]^2 = {0}".format(cMg.value * cOH.value ** 2))
