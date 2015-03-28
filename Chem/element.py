
class Element:
   pass

class KnownElement(Element):
   def __init__(self, z):
      self.__z = z
      
   @property
   def Z(self):
      return self.__z
   
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
         return ElementZLookup[self.Z]
      except KeyError:
         return "Z({0})".format(self.Z)

   def __repr__(self):
      return str(self)

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

ElementZLookup = {
   1: "H",
   2: "He",
   3: "Li",
   4: "Be",
   5: "B",
   6: "C",
   7: "N",
   8: "O",
   9: "F",
   10: "Ne",
   11: "Na",
   12: "Mg",
   13: "Al",
   14: "Si",
   15: "P",
   16: "S",
   17: "Cl",
   18: "Ar",
   19: "K",
   20: "Ca",
   21: "Sc",
   22: "Ti",
   23: "V",
   24: "Cr",
   25: "Mn",
   26: "Fe",
   27: "Co",
   28: "Ni",
   29: "Cu",
   30: "Zn",
   31: "Ga",
   32: "Ge",
   33: "As",
   34: "Se",
   35: "Br",
   36: "Kr",
   37: "Rb",
   38: "Sr",
   39: "Y",
   40: "Zr",
   41: "Nb",
   42: "Mo",
   43: "Tc",
   44: "Ru",
   45: "Rh",
   46: "Pd",
   47: "Ag",
   48: "Cd",
   49: "In",
   50: "Sn",
   51: "Sb",
   52: "Te",
   53: "I",
   54: "Xe",
   55: "Cs",
   56: "Ba",
   57: "La",
   58: "Ce",
   59: "Pr",
   60: "Nd",
   61: "Pm",
   62: "Sm",
   63: "Eu",
   64: "Gd",
   65: "Tb",
   66: "Dy",
   67: "Ho",
   68: "Er",
   69: "Tm",
   70: "Yb",
   71: "Lu",
   72: "Hf",
   73: "Ta",
   74: "W",
   75: "Re",
   76: "Os",
   77: "Ir",
   78: "Pt",
   79: "Au",
   80: "Hg",
   81: "Tl",
   82: "Pb",
   83: "Bi",
   84: "Po",
   85: "At",
   86: "Rn",
   87: "Fr",
   88: "Ra",
   89: "Ac",
   90: "Th",
   91: "Pa",
   92: "U",
   93: "Np",
   94: "Pu",
   95: "Am",
   96: "Cm",
   97: "Bk",
   98: "Cf",
   99: "Es",
   100: "Fm",
   101: "Md",
   102: "No",
   103: "Lr",
   104: "Rf",
   105: "Db",
   106: "Sg",
   107: "Bh",
   108: "Hs",
   109: "Mt",
   110: "Ds",
   111: "Rg",
   112: "Cn",
   113: "Uut",
   114: "Fl",
   115: "Uup",
   116: "Lv",
   117: "Uus",
   118: "Uuo"
}
