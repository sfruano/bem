
import numpy as np  

def Prandtl_corrections(r,R, Rroot, lamda, nblades, a)

""""
r = radial position of the blade
R = Turbine radius
Rroot = Root radius
lamda = Tip speed ratio
nblades = Number of blades 
a = Axial induction 
"""""
ratio = r/R

num1 = -nblades/2*(1-ratio)/ratio*np.sqrt( 1+ ((lamda*ratio)**2)/((1-a)**2))
Ftip = np.array(2/np.pi*np.arccos(np.exp(num1)))

num2 = -nblades/2*(ratio-Rroot)/ratio*np.sqrt( 1+ ((lamda*ratio)**2)/((1-a)**2))
Froot = np.array(2/np.pi*np.arccos(np.exp(num2)))

p_lim = 0.0001
Ftotal = Ftip*Froot
pos = Ftotal < p_lim
Ftotal[pos] = p_lim

return Ftotal Ftip Froot
