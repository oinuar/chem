from element import Molecule
from collections import Counter
from itertools import izip_longest, chain

class Unit:
   def __init__(self, molecule, ratio=1):
      self.__molecule = molecule
      self.__ratio = ratio
   
   @property
   def molecule(self):
      return self.__molecule
   
   @property
   def ratio(self):
      return self.__ratio

   def __hash__(self):
      return hash(tuple(self))
   
   def __iter__(self):
      for i in range(0, self.ratio):
         for x in self.molecule:
            yield x

   def __eq__(self, x):
      return isinstance(x, Unit) and self.ratio == x.ratio and self.molecule == x.molecule

   def __str__(self):
      return "{0}{1}".format(self.ratio if self.ratio != 1 else "", str(self.molecule))
      
   def __repr__(self):
      return self.__str__()

class Reagent:
   def __init__(self, *args, **kwargs):
      self.__unit = Unit(*args, **kwargs)

   @property
   def unit(self):
      return self.__unit

   def copy(self, *args, **kwargs):
      return Reagent(self.unit.molecule, *args, **kwargs)
      
   def __eq__(self, x):
      if isinstance(x, Product):
         return Equation(self, x)

      return NotImplemented

   def __add__(self, x):
      if isinstance(x, Reagent):
         return CompoundReagent(self, x)
      
      return NotImplemented

   def __iter__(self):
      return iter(self.unit)
      
   def __str__(self):
      return str(self.unit)

   def __repr__(self):
      return "Reagent({0})".format(repr(self.unit))
      
class Product:
   def __init__(self, *args, **kwargs):
      self.__unit = Unit(*args, **kwargs)

   @property
   def unit(self):
      return self.__unit

   def copy(self, *args, **kwargs):
      return Product(self.unit.molecule, *args, **kwargs)
      
   def __add__(self, x):
      if isinstance(x, Product):
         return CompoundProduct(self, x)
      
      return NotImplemented

   def __iter__(self):
      return iter(self.unit)

   def __str__(self):
      return str(self.unit)

   def __repr__(self):
      return "Product({0})".format(repr(self.unit))
      
class CompoundReagent(Reagent):
   def __init__(self, lhs, rhs):
      self.__lhs = lhs
      self.__rhs = rhs

   @property
   def unit(self):
      return None

   @property
   def left(self):
      return self.__lhs
      
   @property
   def right(self):
      return self.__rhs

   def __iter__(self):
      return chain(iter(self.left), iter(self.right))
      
   def __str__(self):
      return "{0} + {1}".format(str(self.left), str(self.right))
      
   def __repr__(self):
      return "{0} + {1}".format(repr(self.left), repr(self.right))

class CompoundProduct(Product):
   def __init__(self, lhs, rhs):
      self.__lhs = lhs
      self.__rhs = rhs

   @property
   def unit(self):
      return None

   @property
   def left(self):
      return self.__lhs
      
   @property
   def right(self):
      return self.__rhs
      
   def __iter__(self):
      return chain(iter(self.left), iter(self.right))
      
   def __str__(self):
      return "{0} + {1}".format(str(self.left), str(self.right))

   def __repr__(self):
      return "{0} + {1}".format(repr(self.left), repr(self.right))

class Equation:
   def __init__(self, reagent, product):
      self.__reagent = reagent
      self.__product = product

   @property
   def reagent(self):
      return self.__reagent

   @property
   def product(self):
      return self.__product
   
   def __getitem__(self, molecule):
      molecule = Molecule(molecule)
   
      return self.__find(molecule, self.reagent) or self.__find(molecule, self.product)
   
   def __find(self, molecule, x):
      if isinstance(x, CompoundReagent) or isinstance(x, CompoundProduct):
         return self.__find(molecule, x.left) or self.__find(molecule, x.right)
      
      if (isinstance(x, Product) or isinstance(x, Reagent)) and x.unit.molecule == molecule:
         return x
      
      return None

   def balance(self):
      variables = []
      variable_set = set()
      domain = set()
   
      def collector(x):
         if isinstance(x, CompoundReagent) or isinstance(x, CompoundProduct):
            collector(x.left)
            collector(x.right)
            return
         
         if isinstance(x, Reagent) or isinstance(x, Product):
            variables.append(x)
            domain.add(x.unit.ratio)
            domain.update(Counter(x).values())
      
      def backtrace(assignment):
         eq = make_equation_for_assignment(assignment)
      
         if eq:
            return eq
         
         s = variable_set ^ set(x[0] for x in assignment)
         
         if s:
            k = s.pop()
            variable = variables[k]
            
            for value in domain:
               result = backtrace(assignment + [(k, variable, value)])
               
               if result:
                  return result

         return None
      
      def make_equation_for_assignment(assignment):
         units = [variable.copy(ratio) for (k, variable, ratio) in assignment]
         reagents = [x for x in units if isinstance(x, Reagent)]
         products = [x for x in units if isinstance(x, Product)]
         
         if not reagents or not products:
            return None

         return Equation(reduce(CompoundReagent, reagents), reduce(CompoundProduct, products))
      
      collector(self.reagent)
      collector(self.product)
      
      variable_set.update(x for x in range(0, len(variables)))
      
      eq = backtrace([])
      
      if not eq:
         raise Exception("Equation '{0}' cannot be balanced".format(str(self)))
      
      return eq

   def __bool__(self):
      for (x, y) in izip_longest(sorted(self.reagent), sorted(self.product)):
         if not x or not y or x != y:
            return False

      return True

   def __nonzero__(self):
      return self.__bool__()

   def __str__(self):
      return "{0} -> {1}".format(str(self.reagent), str(self.product))

   def __repr__(self):
      return "{0} -> {1}".format(repr(self.reagent), repr(self.product))
