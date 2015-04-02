from itertools import izip_longest, chain

class Element:
   def __init__(self):
      raise NotImplementedError()

   def __iter__(self):
      # This makes Molecule and Element appear the same,
      # so they can be used through the same interface.
      yield self

class KnownElement(Element):
   def __init__(self, z):
      self.__z = z
      
   @property
   def Z(self):
      return self.__z
   
   @property
   def mass(self):
      return PeriodicTable[self.Z]["AtomicWeight"]

   def __hash__(self):
      return hash(self.Z)
   
   def __eq__(self, x):
      if isinstance(x, KnownElement):
         return self.Z == x.Z
         
      if isinstance(x, Element):
         return False
         
      return NotImplemented

   def __ne__(self, x):
      if isinstance(x, KnownElement):
         return self.Z != x.Z
         
      if isinstance(x, Element):
         return True
         
      return NotImplemented

   def __lt__(self, x):
      if isinstance(x, KnownElement):
         return self.Z < x.Z
         
      return NotImplemented   
      
   def __gt__(self, x):
      if isinstance(x, KnownElement):
         return self.Z > x.Z
         
      return NotImplemented   
   
   def __str__(self):
      try:
         return PeriodicTable[self.Z]["Symbol"]
      except KeyError:
         return "Z({0})".format(self.Z)

   def __repr__(self):
      return str(self)

def Molecule(*args):
   if not args:
      raise ValueError("Expected elements or a molecule")
   
   args = list(args)
   
   for x in args:
      if not isinstance(x, Element):
         if len(args) == 1 and isinstance(x, ElementMolecule):
            return x

         raise ValueError("Got '{0}' but expected Element".format(str(x)))

   return ElementMolecule(*args)

class ElementMolecule:
   def __init__(self, *elements):
      self.__elements = list(elements)

   @property
   def mass(self):
      return sum(x.mass for x in self)

   def __eq__(self, x):
      for (x, y) in izip_longest(self, x):
         if not x or not y or x != y:
            return False
      
      return True

   def __hash__(self):
      return hash(tuple(self.__elements))

   def __iter__(self):
      return iter(self.__elements)
      
   def __str__(self):
      return "".join(map(str, self))

   def __repr__(self):
      return self.__str__()

class Ion:
   def __init__(self, *molecule):
      self.__molecule = Molecule(*molecule)

   @property
   def molecule(self):
      return self.__molecule
      
   def __iter__(self):
      return iter(self.__molecule)

   def __eq__(self, x):
      return isinstance(x, self.__class__) and x.molecule == self.molecule

   def __str__(self):
      return str(self.__molecule)
      
   def __repr__(self):
      return repr(self.__molecule)
      
class Cation(Ion):
   def __init__(self, *args, **kwargs):
      Ion.__init__(self, *args, **kwargs)

   def __hash__(self):
      return Ion.__hash__(self) ^ hash("+")

   def __str__(self):
      return Ion.__str__(self) + "+"
      
   def __repr__(self):
      return Ion.__repr__(self) + "+"

class Anion(Ion):
   def __init__(self, *args, **kwargs):
      Ion.__init__(self, *args, **kwargs)

   def __hash__(self):
      return Ion.__hash__(self) ^ hash("-")

   def __str__(self):
      return Ion.__str__(self) + "-"
      
   def __repr__(self):
      return Ion.__repr__(self) + "-"

Elements = {
   "H": KnownElement(1),
   "He": KnownElement(2),
   "Li": KnownElement(3),
   "Be": KnownElement(4),
   "B": KnownElement(5),
   "C": KnownElement(6),
   "N": KnownElement(7),
   "O": KnownElement(8),
   "F": KnownElement(9),
   "Ne": KnownElement(10),
   "Na": KnownElement(11),
   "Mg": KnownElement(12),
   "Al": KnownElement(13),
   "Si": KnownElement(14),
   "P": KnownElement(15),
   "S": KnownElement(16),
   "Cl": KnownElement(17),
   "Ar": KnownElement(18),
   "K": KnownElement(19),
   "Ca": KnownElement(20),
   "Sc": KnownElement(21),
   "Ti": KnownElement(22),
   "V": KnownElement(23),
   "Cr": KnownElement(24),
   "Mn": KnownElement(25),
   "Fe": KnownElement(26),
   "Co": KnownElement(27),
   "Ni": KnownElement(28),
   "Cu": KnownElement(29),
   "Zn": KnownElement(30),
   "Ga": KnownElement(31),
   "Ge": KnownElement(32),
   "As": KnownElement(33),
   "Se": KnownElement(34),
   "Br": KnownElement(35),
   "Kr": KnownElement(36),
   "Rb": KnownElement(37),
   "Sr": KnownElement(38),
   "Y": KnownElement(39),
   "Zr": KnownElement(40),
   "Nb": KnownElement(41),
   "Mo": KnownElement(42),
   "Tc": KnownElement(43),
   "Ru": KnownElement(44),
   "Rh": KnownElement(45),
   "Pd": KnownElement(46),
   "Ag": KnownElement(47),
   "Cd": KnownElement(48),
   "In": KnownElement(49),
   "Sn": KnownElement(50),
   "Sb": KnownElement(51),
   "Te": KnownElement(52),
   "I": KnownElement(53),
   "Xe": KnownElement(54),
   "Cs": KnownElement(55),
   "Ba": KnownElement(56),
   "La": KnownElement(57),
   "Ce": KnownElement(58),
   "Pr": KnownElement(59),
   "Nd": KnownElement(60),
   "Pm": KnownElement(61),
   "Sm": KnownElement(62),
   "Eu": KnownElement(63),
   "Gd": KnownElement(64),
   "Tb": KnownElement(65),
   "Dy": KnownElement(66),
   "Ho": KnownElement(67),
   "Er": KnownElement(68),
   "Tm": KnownElement(69),
   "Yb": KnownElement(70),
   "Lu": KnownElement(71),
   "Hf": KnownElement(72),
   "Ta": KnownElement(73),
   "W": KnownElement(74),
   "Re": KnownElement(75),
   "Os": KnownElement(76),
   "Ir": KnownElement(77),
   "Pt": KnownElement(78),
   "Au": KnownElement(79),
   "Hg": KnownElement(80),
   "Tl": KnownElement(81),
   "Pb": KnownElement(82),
   "Bi": KnownElement(83),
   "Po": KnownElement(84),
   "At": KnownElement(85),
   "Rn": KnownElement(86),
   "Fr": KnownElement(87),
   "Ra": KnownElement(88),
   "Ac": KnownElement(89),
   "Th": KnownElement(90),
   "Pa": KnownElement(91),
   "U": KnownElement(92),
   "Np": KnownElement(93),
   "Pu": KnownElement(94),
   "Am": KnownElement(95),
   "Cm": KnownElement(96),
   "Bk": KnownElement(97),
   "Cf": KnownElement(98),
   "Es": KnownElement(99),
   "Fm": KnownElement(100),
   "Md": KnownElement(101),
   "No": KnownElement(102),
   "Lr": KnownElement(103),
   "Rf": KnownElement(104),
   "Db": KnownElement(105),
   "Sg": KnownElement(106),
   "Bh": KnownElement(107),
   "Hs": KnownElement(108),
   "Mt": KnownElement(109),
   "Ds": KnownElement(110),
   "Rg": KnownElement(111),
   "Cn": KnownElement(112),
   "Uut": KnownElement(113),
   "Fl": KnownElement(114),
   "Uup": KnownElement(115),
   "Lv": KnownElement(116),
   "Uus": KnownElement(117),
   "Uuo": KnownElement(118)
}

PeriodicTable = {
   1: {"Symbol": "H", "Group": 1, "Period": 1, "AtomicWeight": 1.008},
   2: {"Symbol": "He", "Group": 18, "Period": 1, "AtomicWeight": 4.0026022},
   3: {"Symbol": "Li", "Group": 1, "Period": 2, "AtomicWeight": 6.94},
   4: {"Symbol": "Be", "Group": 2, "Period": 2, "AtomicWeight": 9.0121823},
   5: {"Symbol": "B", "Group": 13, "Period": 2, "AtomicWeight": 10.81222333444},
   6: {"Symbol": "C", "Group": 14, "Period": 2, "AtomicWeight": 12.011222444},
   7: {"Symbol": "N", "Group": 15, "Period": 2, "AtomicWeight": 14.007222444},
   8: {"Symbol": "O", "Group": 16, "Period": 2, "AtomicWeight": 15.999222444},
   9: {"Symbol": "F", "Group": 17, "Period": 2, "AtomicWeight": 18.99840325},
   10: {"Symbol": "Ne", "Group": 18, "Period": 2, "AtomicWeight": 20.17976222333},
   11: {"Symbol": "Na", "Group": 1, "Period": 3, "AtomicWeight": 22.989769282},
   12: {"Symbol": "Mg", "Group": 2, "Period": 3, "AtomicWeight": 24.305},
   13: {"Symbol": "Al", "Group": 13, "Period": 3, "AtomicWeight": 26.98153868},
   14: {"Symbol": "Si", "Group": 14, "Period": 3, "AtomicWeight": 28.085},
   15: {"Symbol": "P", "Group": 15, "Period": 3, "AtomicWeight": 30.9737622},
   16: {"Symbol": "S", "Group": 16, "Period": 3, "AtomicWeight": 32.06},
   17: {"Symbol": "Cl", "Group": 17, "Period": 3, "AtomicWeight": 35.45},
   18: {"Symbol": "Ar", "Group": 18, "Period": 3, "AtomicWeight": 39.9481},
   19: {"Symbol": "K", "Group": 1, "Period": 4, "AtomicWeight": 39.09831},
   20: {"Symbol": "Ca", "Group": 2, "Period": 4, "AtomicWeight": 40.0784},
   21: {"Symbol": "Sc", "Group": 3, "Period": 4, "AtomicWeight": 44.9559126},
   22: {"Symbol": "Ti", "Group": 4, "Period": 4, "AtomicWeight": 47.8671},
   23: {"Symbol": "V", "Group": 5, "Period": 4, "AtomicWeight": 50.94151},
   24: {"Symbol": "Cr", "Group": 6, "Period": 4, "AtomicWeight": 51.99616},
   25: {"Symbol": "Mn", "Group": 7, "Period": 4, "AtomicWeight": 54.9380455},
   26: {"Symbol": "Fe", "Group": 8, "Period": 4, "AtomicWeight": 55.8452},
   27: {"Symbol": "Co", "Group": 9, "Period": 4, "AtomicWeight": 58.9331955},
   28: {"Symbol": "Ni", "Group": 10, "Period": 4, "AtomicWeight": 58.69344},
   29: {"Symbol": "Cu", "Group": 11, "Period": 4, "AtomicWeight": 63.5463},
   30: {"Symbol": "Zn", "Group": 12, "Period": 4, "AtomicWeight": 65.382},
   31: {"Symbol": "Ga", "Group": 13, "Period": 4, "AtomicWeight": 69.7231},
   32: {"Symbol": "Ge", "Group": 14, "Period": 4, "AtomicWeight": 72.6308},
   33: {"Symbol": "As", "Group": 15, "Period": 4, "AtomicWeight": 74.921602},
   34: {"Symbol": "Se", "Group": 16, "Period": 4, "AtomicWeight": 78.963},
   35: {"Symbol": "Br", "Group": 17, "Period": 4, "AtomicWeight": 79.904},
   36: {"Symbol": "Kr", "Group": 18, "Period": 4, "AtomicWeight": 83.7982},
   37: {"Symbol": "Rb", "Group": 1, "Period": 5, "AtomicWeight": 85.46783},
   38: {"Symbol": "Sr", "Group": 2, "Period": 5, "AtomicWeight": 87.621},
   39: {"Symbol": "Y", "Group": 3, "Period": 5, "AtomicWeight": 88.905852},
   40: {"Symbol": "Zr", "Group": 4, "Period": 5, "AtomicWeight": 91.2242},
   41: {"Symbol": "Nb", "Group": 5, "Period": 5, "AtomicWeight": 92.906382},
   42: {"Symbol": "Mo", "Group": 6, "Period": 5, "AtomicWeight": 95.962},
   43: {"Symbol": "Tc", "Group": 7, "Period": 5, "AtomicWeight": 98111},
   44: {"Symbol": "Ru", "Group": 8, "Period": 5, "AtomicWeight": 101.072222},
   45: {"Symbol": "Rh", "Group": 9, "Period": 5, "AtomicWeight": 102.905502},
   46: {"Symbol": "Pd", "Group": 10, "Period": 5, "AtomicWeight": 106.421222},
   47: {"Symbol": "Ag", "Group": 11, "Period": 5, "AtomicWeight": 107.86822222},
   48: {"Symbol": "Cd", "Group": 12, "Period": 5, "AtomicWeight": 112.4118222},
   49: {"Symbol": "In", "Group": 13, "Period": 5, "AtomicWeight": 114.8181},
   50: {"Symbol": "Sn", "Group": 14, "Period": 5, "AtomicWeight": 118.7107222},
   51: {"Symbol": "Sb", "Group": 15, "Period": 5, "AtomicWeight": 121.7601222},
   52: {"Symbol": "Te", "Group": 16, "Period": 5, "AtomicWeight": 127.603222},
   53: {"Symbol": "I", "Group": 17, "Period": 5, "AtomicWeight": 126.904473},
   54: {"Symbol": "Xe", "Group": 18, "Period": 5, "AtomicWeight": 131.2936222333},
   55: {"Symbol": "Cs", "Group": 1, "Period": 6, "AtomicWeight": 132.90545192},
   56: {"Symbol": "Ba", "Group": 2, "Period": 6, "AtomicWeight": 137.3277},
   57: {"Symbol": "La", "Group": None, "Period": 6, "AtomicWeight": 138.905477222},
   58: {"Symbol": "Ce", "Group": None, "Period": 6, "AtomicWeight": 140.1161222},
   59: {"Symbol": "Pr", "Group": None, "Period": 6, "AtomicWeight": 140.907652},
   60: {"Symbol": "Nd", "Group": None, "Period": 6, "AtomicWeight": 144.2423222},
   61: {"Symbol": "Pm", "Group": None, "Period": 6, "AtomicWeight": 145111},
   62: {"Symbol": "Sm", "Group": None, "Period": 6, "AtomicWeight": 150.362222},
   63: {"Symbol": "Eu", "Group": None, "Period": 6, "AtomicWeight": 151.9641222},
   64: {"Symbol": "Gd", "Group": None, "Period": 6, "AtomicWeight": 157.253222},
   65: {"Symbol": "Tb", "Group": None, "Period": 6, "AtomicWeight": 158.925352},
   66: {"Symbol": "Dy", "Group": None, "Period": 6, "AtomicWeight": 162.5001222},
   67: {"Symbol": "Ho", "Group": None, "Period": 6, "AtomicWeight": 164.930322},
   68: {"Symbol": "Er", "Group": None, "Period": 6, "AtomicWeight": 167.2593222},
   69: {"Symbol": "Tm", "Group": None, "Period": 6, "AtomicWeight": 168.934212},
   70: {"Symbol": "Yb", "Group": None, "Period": 6, "AtomicWeight": 173.0545222},
   71: {"Symbol": "Lu", "Group": 3, "Period": 6, "AtomicWeight": 174.96681222},
   72: {"Symbol": "Hf", "Group": 4, "Period": 6, "AtomicWeight": 178.492},
   73: {"Symbol": "Ta", "Group": 5, "Period": 6, "AtomicWeight": 180.947882},
   74: {"Symbol": "W", "Group": 6, "Period": 6, "AtomicWeight": 183.841},
   75: {"Symbol": "Re", "Group": 7, "Period": 6, "AtomicWeight": 186.2071},
   76: {"Symbol": "Os", "Group": 8, "Period": 6, "AtomicWeight": 190.233222},
   77: {"Symbol": "Ir", "Group": 9, "Period": 6, "AtomicWeight": 192.2173},
   78: {"Symbol": "Pt", "Group": 10, "Period": 6, "AtomicWeight": 195.0849},
   79: {"Symbol": "Au", "Group": 11, "Period": 6, "AtomicWeight": 196.9665694},
   80: {"Symbol": "Hg", "Group": 12, "Period": 6, "AtomicWeight": 200.5923},
   81: {"Symbol": "Tl", "Group": 13, "Period": 6, "AtomicWeight": 204.38999},
   82: {"Symbol": "Pb", "Group": 14, "Period": 6, "AtomicWeight": 207.21222444},
   83: {"Symbol": "Bi", "Group": 15, "Period": 6, "AtomicWeight": 208.980401111},
   84: {"Symbol": "Po", "Group": 16, "Period": 6, "AtomicWeight": 209},
   85: {"Symbol": "At", "Group": 17, "Period": 6, "AtomicWeight": 210},
   86: {"Symbol": "Rn", "Group": 18, "Period": 6, "AtomicWeight": 222},
   87: {"Symbol": "Fr", "Group": 1, "Period": 7, "AtomicWeight": 223111},
   88: {"Symbol": "Ra", "Group": 2, "Period": 7, "AtomicWeight": 226},
   89: {"Symbol": "Ac", "Group": None, "Period": 7, "AtomicWeight": 227},
   90: {"Symbol": "Th", "Group": None, "Period": 7, "AtomicWeight": 232.038062111222},
   91: {"Symbol": "Pa", "Group": None, "Period": 7, "AtomicWeight": 231.035882111},
   92: {"Symbol": "U", "Group": None, "Period": 7, "AtomicWeight": 238.028913111},
   93: {"Symbol": "Np", "Group": None, "Period": 7, "AtomicWeight": 237},
   94: {"Symbol": "Pu", "Group": None, "Period": 7, "AtomicWeight": 244},
   95: {"Symbol": "Am", "Group": None, "Period": 7, "AtomicWeight": 243},
   96: {"Symbol": "Cm", "Group": None, "Period": 7, "AtomicWeight": 247},
   97: {"Symbol": "Bk", "Group": None, "Period": 7, "AtomicWeight": 247},
   98: {"Symbol": "Cf", "Group": None, "Period": 7, "AtomicWeight": 251},
   99: {"Symbol": "Es", "Group": None, "Period": 7, "AtomicWeight": 252},
   100: {"Symbol": "Fm", "Group": None, "Period": 7, "AtomicWeight": 257},
   101: {"Symbol": "Md", "Group": None, "Period": 7, "AtomicWeight": 258},
   102: {"Symbol": "No", "Group": None, "Period": 7, "AtomicWeight": 259},
   103: {"Symbol": "Lr", "Group": 3, "Period": 7, "AtomicWeight": 266},
   104: {"Symbol": "Rf", "Group": 4, "Period": 7, "AtomicWeight": 267},
   105: {"Symbol": "Db", "Group": 5, "Period": 7, "AtomicWeight": 268},
   106: {"Symbol": "Sg", "Group": 6, "Period": 7, "AtomicWeight": 269},
   107: {"Symbol": "Bh", "Group": 7, "Period": 7, "AtomicWeight": 270},
   108: {"Symbol": "Hs", "Group": 8, "Period": 7, "AtomicWeight": 269},
   109: {"Symbol": "Mt", "Group": 9, "Period": 7, "AtomicWeight": 278},
   110: {"Symbol": "Ds", "Group": 10, "Period": 7, "AtomicWeight": 281},
   111: {"Symbol": "Rg", "Group": 11, "Period": 7, "AtomicWeight": 281},
   112: {"Symbol": "Cn", "Group": 12, "Period": 7, "AtomicWeight": 285},
   113: {"Symbol": "Uut", "Group": 13, "Period": 7, "AtomicWeight": 286},
   114: {"Symbol": "Fl", "Group": 14, "Period": 7, "AtomicWeight": 289},
   115: {"Symbol": "Uup", "Group": 15, "Period": 7, "AtomicWeight": 289},
   116: {"Symbol": "Lv", "Group": 16, "Period": 7, "AtomicWeight": 293},
   117: {"Symbol": "Uus", "Group": 17, "Period": 7, "AtomicWeight": 294},
   118: {"Symbol": "Uuo", "Group": 18, "Period": 7, "AtomicWeight": 294}
}
