
class Molecule:
   def __init__(self, *args):
      self.__elements = list(args)

   def __iter__(self):
      return iter(self.__elements)
      
   def __str__(self):
      return "".join(map(str, self))
