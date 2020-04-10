#
# ---------------------------------------------------------------------------------------------
# test.py
# ---------------------------------------------------------------------------------------------

class SomeClass:
	
	CONST1 = "TEST"
	CONST2 = "BUNNY"
	CONST3 = CONST1 + CONST2
	
	var1   = None
	
	def __init__(self,xx):
		self.Var1 = xx
		
	def goo(self):
		return self.CONST3
		
print("GOO: " + SomeClass.CONST3)