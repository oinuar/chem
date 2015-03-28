
class Sieve:
   def __init__(self, equation):
      if not equation:
         raise ValueError("Equation '{0}' is not valid".format(str(equation)))

      self.__eq = equation

class Unit:
   def __init__(self, molecule, amount):
      self.__molecule = molecule
      self.__amount = amount
      
   @property
   def molecule(self):
      return self.__molecule
      
   @property
   def amount(self):
      return self.__amount
   
   def __str__(self):
      return "{0} ({1:.3f} {2})".format(str(self.molecule), self.amount, self._symbol)
      
   def __repr__(self):
      return "{0}[{1}]({2:.3f})".format(self.__class__.__name__, str(self.molecule), self.amount)
      
class Moles(Unit):
   def __init__(self, *args, **kwargs):
      Unit.__init__(self, *args, **kwargs)
   
   @property
   def moles(self):
      return self

   @property
   def grams(self):
      return Grams(self.molecule, self.amount * self.molecule.mass)
      
   @property
   def _symbol(self):
      return "mol"

class Grams(Unit):
   def __init__(self, *args, **kwargs):
      Unit.__init__(self, *args, **kwargs)
   
   @property
   def moles(self):
      return Moles(self.molecule, self.amount / self.molecule.mass)

   @property
   def grams(self):
      return self

   @property
   def _symbol(self):
      return "g"
