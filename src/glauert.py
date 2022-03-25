
from numpy  import ndarray, sqrt, zeros


def glauertCorrection(ct: ndarray) -> ndarray:
    """
    Parameters
    ----------
    Ct : int
        Thrust coefficient

    Returns
    -------
    a: ndarray
        induction  factor

    """

    ct1 = 1.816
    ct2 = 2*sqrt(ct1)-ct1

    a = zeros(ct.shape)
    pos = ct < ct2
    a[pos] = 0.5 - sqrt(1-ct[pos])/2.0
    pos = ct >= ct2
    a[pos] = 1+(ct[pos]-ct1)/4.0/(sqrt(ct1)-1.0)

    return a