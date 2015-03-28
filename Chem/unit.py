from molecule import Molecule
from collections import Counter

class Unit:
   def __init__(self, molecule, ratio=1):
      self.__molecule = molecule
      self.__n = ratio
      
      if not isinstance(self.__n, int):
         raise TypeError("'ratio' must be integer")
      
      if self.__n <= 0:
         raise ValueError("'ratio' cannot be negative or zero")
      
   @property
   def ratio(self):
      return self.__n

   @property
   def molecule(self):
      return self.__molecule
      
   def copy(self, n):
      return Unit(self.molecule, n)
      
   def accept(self, visitor):
      return visitor.visit_unit(self)
   
   def __hash__(self):
      return hash(tuple(self))
   
   def __iter__(self):
      for i in range(0, self.ratio):
         for x in self.molecule:
            yield x

   def __str__(self):
      return "{0}{1}".format(self.ratio if self.ratio != 1 else "", str(self.molecule))
      
   def __repr__(self):
      return repr(map(repr, self))

class Reagent(Unit):
   def __init__(self, *args, **kwargs):
      Unit.__init__(self, *args, **kwargs)

   def accept(self, visitor):
      return visitor.visit_reagent(self)
      
   def copy(self, n):
      return Reagent(self.molecule, n)
      
   def __add__(self, x):
      if not isinstance(x, Reagent):
         return NotImplemented
      
      return CompoundReagent(self, x)
      
   def __eq__(self, x):
      if not isinstance(x, Product):
         return NotImplemented
      
      return Equation(self, x)

class CompoundReagent(Reagent):
   def __init__(self, lhs, rhs):
      Reagent.__init__(self, Molecule(*(list(lhs) + list(rhs))))
      self.__lhs = lhs
      self.__rhs = rhs
   
   @property
   def left(self):
      return self.__lhs
   
   @property
   def right(self):
      return self.__rhs
   
   def accept(self, visitor):
      return visitor.visit_compound_reagent(self)
      
   def __str__(self):
      return "{0} + {1}".format(str(self.left), str(self.right))

   def __repr__(self):
      return "{0} + {1}".format(repr(self.left), repr(self.right))

class Product(Unit):
   def __init__(self, *args, **kwargs):
      Unit.__init__(self, *args, **kwargs)
   
   def accept(self, visitor):
      return visitor.visit_product(self)
      
   def copy(self, n):
      return Product(self.molecule, n)
      
   def __add__(self, x):
      if not isinstance(x, Product):
         return NotImplemented
      
      return CompoundProduct(self, x)

class CompoundProduct(Product):
   def __init__(self, lhs, rhs):
      Product.__init__(self, Molecule(*(list(lhs) + list(rhs))))
      self.__lhs = lhs
      self.__rhs = rhs
      
   @property
   def left(self):
      return self.__lhs
   
   @property
   def right(self):
      return self.__rhs
   
   def accept(self, visitor):
      return visitor.visit_compound_product(self)
      
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
   
   def balance(self):
      variables = []
      variable_set = set()
      domain = set()
   
      def collector(x):
         variables.append(x)
         domain.add(x.ratio)
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
      
      visitor = UnitVisitor(collector)
      
      self.reagent.accept(visitor)
      self.product.accept(visitor)
      
      variable_set.update(x for x in range(0, len(variables)))
      
      eq = backtrace([])
      
      if not eq:
         raise Exception("Equation '{0}' cannot be balanced".format(str(self)))
      
      return eq
   
   def __bool__(self):
      reagents = list(self.reagent)
      products = list(self.product)

      if len(reagents) != len(products):
         return False

      reagents.sort()
      products.sort()

      for i in range(0, len(products)):
         if reagents[i] != products[i]:
            return False

      return True

   def __nonzero__(self):
      return self.__bool__()
      
   def __str__(self):
      return "{0} -> {1}".format(str(self.reagent), str(self.product))

   def __repr__(self):
      return "{0} -> {1}".format(repr(self.reagent), repr(self.product))

class Visitor:
   def visit_unit(self, x):
      return x
   
   def visit_reagent(self, x):
      return self.visit_unit(x)
      
   def visit_compound_reagent(self, x):
      lhs = x.left.accept(self)
      rhs = x.right.accept(self)
      
      if lhs != x.left or rhs != x.right:
         return CompoundReagent(lhs, rhs)
      
      return x
   
   def visit_product(self, x):
      return self.visit_unit(x)
   
   def visit_compound_product(self, x):
      lhs = x.left.accept(self)
      rhs = x.right.accept(self)
      
      if lhs != x.left or rhs != x.right:
         return CompoundProduct(lhs, rhs)
      
      return x
      
class UnitVisitor(Visitor):
   def __init__(self, callback):
      self.__callback = callback

   def visit_unit(self, x):
      result = self.__callback(x)
      
      return result if result else x
