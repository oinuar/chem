from element import Molecule
from itertools import chain

class Sieve:
   def __init__(self, equation, size, *args):
      if not equation:
         raise ValueError("Equation '{0}' is not valid".format(str(equation)))

      self.__eq = equation
      self.__size = size
      self.__contents = {}
      
      for x in args:
         if x.molecule in self.__contents:
            self.__contents[x.molecule] += x.moles
         else:
            self.__contents[x.molecule] = x.moles

   def how_much(self, *molecule):
      molecule = Molecule(*molecule)
      unit = self.__eq[molecule]
      
      if unit:
         for (k, v) in self.__contents.items():
            reference = self.__eq[k]
            
            if reference:
               return v.copy(v.moles * (unit.unit.ratio / float(reference.unit.ratio)))

      raise Exception("Cannot figure out how much '{0}'".format(str(molecule)))

   def __add__(self, x):
      if not isinstance(x, self.__class__):
         x = [x]

      return Sieve(self.__eq, self.__size, *chain(self, x))

   def __getitem__(self, molecule):
      molecule = Molecule(molecule)

      try:
         content = self.__contents[molecule]
      except KeyError:
         content = Moles(molecule, 0)

      return Concentration(self.__size, content)

   def __iter__(self):
      return iter(self.__contents.values())
      
   def __repr__(self):
      return "Sieve[{0}]({1}, {2})".format(str(self.__eq), self.__size, repr(dict(self.__contents)))

class MoleculeUnit:
   def __init__(self, molecule, amount):
      self.__molecule = Molecule(molecule)
      self.__amount = amount
      
   @property
   def molecule(self):
      return self.__molecule
      
   @property
   def value(self):
      return self.__amount

   def copy(self, amount):
      return MoleculeUnit(self.molecule, amount)
   
   @property
   def _symbol(self):
      return None
      
   def __wrap(self, op, x):
      if isinstance(x, self.__class__):
         return self.copy(op(x.value))
      
      return op(x)

   def __add__(self, x):
      return self.__wrap(lambda y: self.value + y, x)

   def __sub__(self, x):
      return self.__wrap(lambda y: self.value - y, x)

   def __mul__(self, x):
      return self.__wrap(lambda y: self.value * y, x)
      
   def __div__(self, x):
      return self.__wrap(lambda y: self.value / y, x)

   def __truediv__(self, x):
      return self.__div__(x)

   def __pow__(self, x):
      return self.__wrap(lambda y: self.value ** y, x)

   def __str__(self):
      symbol = self._symbol
      return "{0} ({1:.3e}{2}{3})".format(str(self.molecule), self.value, " " if symbol else None, symbol)
      
   def __repr__(self):
      return "{0}[{1}]({2:.3e})".format(self.__class__.__name__, str(self.molecule), self.value)
      
class Moles(MoleculeUnit):
   def __init__(self, *args, **kwargs):
      MoleculeUnit.__init__(self, *args, **kwargs)
   
   @property
   def moles(self):
      return self

   @property
   def grams(self):
      return Grams(self.molecule, self.value * self.molecule.mass)
      
   def copy(self, amount):
      return Moles(self.molecule, amount)
      
   @property
   def _symbol(self):
      return "mol"

class Grams(MoleculeUnit):
   def __init__(self, *args, **kwargs):
      MoleculeUnit.__init__(self, *args, **kwargs)
   
   @property
   def moles(self):
      return Moles(self.molecule, self.value / self.molecule.mass)

   @property
   def grams(self):
      return self

   def copy(self, amount):
      return Grams(self.molecule, amount)
      
   @property
   def _symbol(self):
      return "g"

class Concentration:
   def __init__(self, size, content):
      if size <= 0:
         raise ValueError("'size' cannot be negative or zero")

      self.__size = size
      self.__content = content

   @property
   def size(self):
      return self.__size
      
   @property
   def content(self):
      return self.__content

   @property
   def value(self):
      return self.content.moles / self.size

   def __str__(self):
      return "[{0:.3f} M of {1}]".format(self.value, str(self.content))
      
   def __repr__(self):
      return "Concentration({0:.3f} M, {1})".format(self.value, repr(self.content))
