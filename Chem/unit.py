from molecule import Molecule
from collections import Counter
from copy import deepcopy

class Unit:
   def __init__(self, molecule, n=1):
      self.__molecule = molecule
      self.__n = n
      
   @property
   def ratio(self):
      return self.__n

   @property
   def molecule(self):
      return self.__molecule
      
   def accept(self, visitor):
      return visitor.visit_unit(self)
   
   def __hash__(self):
      return hash(tuple(self))
   
   def __iter__(self):
      for i in range(0, self.ratio):
         for x in self.molecule:
            yield x

   def __str__(self):
      return "{0}{1}".format(self.ratio, str(self.molecule))
      
   def __repr__(self):
      return repr(map(repr, self))

class Reagent(Unit):
   def __init__(self, *args, **kwargs):
      Unit.__init__(self, *args, **kwargs)

   def accept(self, visitor):
      return visitor.visit_reagent(self)
      
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
      class Collector(UnitVisitor):
         def __init__(self):
            self.__variables = []
            self.__domain = set()
     
         @property
         def variables(self):
            return self.__variables
            
         @property
         def domain(self):
            return self.__domain
     
         def __collect(self, x):   
            self.__variables.append(x)
            self.__domain.add(x.ratio)
            self.__domain.update(Counter(x).values())
            return x
     
         def visit_reagent(self, x):
            return self.__collect(x)
            
         def visit_product(self, x):
            return self.__collect(x)
     
      def backtrace(csp, assignment, variable_set):
         if is_complete(assignment):
            return assignment
         
         s = variable_set ^ set(x[0] for x in assignment)
         
         if s:
            k = s.pop()
            
            variable = csp.variables[k]
            
            for value in csp.domain:
               result = backtrace(csp, assignment + [(k, variable, value)], variable_set)
               
               if result is not None:
                  return result
            
         return None
      
      def is_complete(assignment):
         """ The assignment is complete if both sides are equal """
         map = {}
         
         if not assignment:
            return False
         
         for (k, variable, ratio) in assignment:
            new_unit = Unit(variable.molecule, ratio)
            factor = 0
            
            if isinstance(variable, Reagent):
               factor = -1
            elif isinstance(variable, Product):
               factor = 1
            
            for y in new_unit:
               if y in map:
                  map[y] += factor
               else:
                  map[y] = factor

         return all(x == 0 for x in map.values())
      
      collector = Collector()
      eq = deepcopy(self)
      
      eq.reagent.accept(collector)
      eq.product.accept(collector)
      
      assignment = backtrace(collector, [], set(x for x in range(0, len(collector.variables))))
      
      if not assignment:
         raise Error("Equation {0} cannot be balanced".format(str(eq)))
      
      for (k, variable, ratio) in assignment:
         variable.ratio = ratio
      
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
      
   def __str__(self):
      return "{0} -> {1}".format(str(self.reagent), str(self.product))

   def __repr__(self):
      return "{0} -> {1}".format(repr(self.reagent), repr(self.product))

class UnitVisitor:
   def visit_unit(self, x):
      return x
   
   def visit_reagent(self, x):
      return x
      
   def visit_compound_reagent(self, x):
      lhs = x.left.accept(self)
      rhs = x.right.accept(self)
      
      if lhs != x.left or rhs != x.right:
         return CompoundReagent(lhs, rhs)
      
      return x
   
   def visit_product(self, x):
      return x
   
   def visit_compound_product(self, x):
      lhs = x.left.accept(self)
      rhs = x.right.accept(self)
      
      if lhs != x.left or rhs != x.right:
         return CompoundProduct(lhs, rhs)
      
      return x      