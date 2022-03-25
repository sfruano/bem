
from numpy import arccos, exp, ndarray, sqrt, pi


def prandtlCorrection(B: int, lmb: float, R: float, r: ndarray, mu_root: ndarray, a: ndarray) -> ndarray:
    """
    Parameters
    ----------
    B : int
        Number of blades
    lmb : float
        Tip Speed Ratio
    R : float
        Turbine radius
    r : ndarray
        Radial position  of the blade elements center.
    mu_root : float
        Non-dimensional radial starting point of the blade over the turbine radius.
    a : ndarray
        Axial induction factor

    Returns
    -------
    f_total: ndarray
        Prandt total (tip+root) correction factor.

    """

    mu = r/R

    # Calculate tip and root correction
    f_tip = 2/pi*arccos(exp(-B/2.0*((1-mu)/mu)*sqrt(1+(((lmb*mu)**2.0)/((1-a)**2.0)))))
    f_root = 2/pi*arccos(exp(-B/2.0*(mu-mu_root)/mu*sqrt(1+(((lmb*mu)**2.0)/((1-a)**2.0)))))

    # Calculate total Prandtl correction
    p_lim = 0.0001
    f_total = f_tip*f_root
    pos = f_total < p_lim
    f_total[pos] = p_lim
    
    return f_total