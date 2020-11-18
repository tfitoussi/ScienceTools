#=============================================================================#
#
#   Convert particle name in its 2012 Monte Carlo nuclear code schemei (HepID). 
#   Ion numbers are +/- 10LZZZAAAI. 
#       AAA is A - total baryon number 
#       ZZZ is Z - total charge 
#       L is the total number of strange quarks. 
#       I is the isomer number, with I=0 corresponding to the ground state. 
#
#=============================================================================#
from collections import OrderedDict

PeriodicTable = OrderedDict()
PeriodicTable['H']  = 1000010010
PeriodicTable['He'] = 1000020040
PeriodicTable['Li'] = 1000030070
PeriodicTable['Be'] = 1000040090
PeriodicTable['B']  = 1000050110
PeriodicTable['C']  = 1000060120
PeriodicTable['N']  = 1000070140
PeriodicTable['O']  = 1000080160
PeriodicTable['F']  = 1000090190
PeriodicTable['Ne'] = 1000100200
PeriodicTable['Na'] = 1000110230
PeriodicTable['Mg'] = 1000120240
PeriodicTable['Al'] = 1000130270
PeriodicTable['Si'] = 1000140280
PeriodicTable['P']  = 1000150310
PeriodicTable['S']  = 1000160320
PeriodicTable['Cl'] = 1000170350
PeriodicTable['Ar'] = 1000180400
PeriodicTable['K']  = 1000190390
PeriodicTable['Ca'] = 1000200400
PeriodicTable['Sc'] = 1000210450
PeriodicTable['Ti'] = 1000220480
PeriodicTable['V']  = 1000230510
PeriodicTable['Cr'] = 1000240520
PeriodicTable['Mn'] = 1000250550
PeriodicTable['Fe'] = 1000260560
