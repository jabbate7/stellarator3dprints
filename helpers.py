from scipy.integrate import odeint
from scipy.special import iv, modstruve

# The Princeton Dee, see http://www.jaschwartz.net/journal/princeton-dee.html
# y' = ln(x)/k  /  ( 1-(ln(x)/k)^2 )^(1/2); y(1)=-1/2 pi k BesselI(1,k)+StruveL(-1,k)
# for y in range(exp^-k+eps, exp(k)-eps)
def halfSupportCylHeight(k):
    return np.pi * k * iv(1,k)
def dydt(y,t,k):
    num = np.log(t) / k
    denom = (1-num**2)**(0.5)
    dydt = num/denom
    return dydt

def getDeePoints(k, nPointsPerQuadrant=100, eps=1e-7):
    tLeft = np.linspace(1,np.exp(-k)+eps,nPointsPerQuadrant)
    tRight = np.linspace(1,np.exp(k)-eps,nPointsPerQuadrant)
    yAt1=-0.5 * np.pi * k * (iv(1,k) + modstruve(-1,k))
    deeBottomLeft = odeint(dydt,yAt1,tLeft,args=(k,))
    deeBottomRight = odeint(dydt,yAt1,tRight,args=(k,))
    deeTopLeft = -deeBottomLeft
    deeTopRight = -deeBottomRight
    return np.dstack([np.concatenate([tLeft,
                                      np.flip(tLeft),
                                      tRight,
                                      np.flip(tRight)]),
                      np.concatenate([deeTopLeft,
                                      np.flip(deeBottomLeft),
                                      deeBottomRight,
                                      np.flip(deeTopRight)]).flatten()]).squeeze()
