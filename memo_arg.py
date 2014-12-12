from collections import namedtuple
def zzz( x, y ):
    print 'x',x
    print 'y',y

z = {'x':1, 'y':2 }

Arg = namedtuple('Arg', 'y x')

arg = Arg(1,3)

print arg 

zzz(*arg)
zzz(**arg._asdict() )

zzz(**z)
