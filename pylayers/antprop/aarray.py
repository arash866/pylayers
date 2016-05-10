# -*- coding:Utf-8 -*-
import numpy as np
import pylayers.antprop.antenna as ant
import matplotlib.pyplot as plt
import doctest
r"""

.. currentmodule:: pylayers.antprop.aarray

This module handles antenna arrays

Array class
===========

.. autosummary::
    :toctree: generated/

ULAarray class
==============

.. autosummary::
    :toctree: generated/

AntArray class
==============

.. autosummary::
    :toctree: generated/

"""
class TXRU(object):
    """ Tranceiver Units

    See : Y-Han Nam , Saifur Rahman, Yang Li : Full Dimension MIMO for LTE-Advanced and 5G

    """
    def __init__(self):
        pass

class Array(ant.Pattern):
    """ Array class

    An array is defined as the association of a set of points and a set of
    exitations

    """

    def __init__(self,p,w=[],fGHz=np.linspace(1.8,2.2,20)):
        """

        Parameters
        ----------

        p  : set of 3D points (3xNp)   or  3 x Nx x Ny x Nz
        w  : set of weight Np x Nf
                       or  Nx x Ny x Nz x Nf

        fGhz : np.array
            frequency in GHz

        """
        assert type(p)==np.ndarray," Array not an array"
        assert p.shape[0]==3," Array not a 3D point"

        self.p = p
        self.fGHz = fGHz
        shp = np.shape(p)

        # If no excitation choose uniform excitation
        # Np x Nf
        if w == []:
            w = np.ones((shp[1:]))[...,None]
        self.w = w

        self.typ = 'Array'
        self.param={'param':{}}

        ant.Pattern.__init__(self)


    def __add__(self,Aa):

        Anew = Array()
        assert((self.fGHz==Aa.fGHz).all())
        assert((self.p.ndim==2) and (Aa.p.ndim==2))
        Anew.p = np.concatenate(self.p,Aa.p,axis=1)
        Anew.w = np.concatenate(self.w,Aa.w,axis=0)
        
        return(Anew)

    def __repr__(self):
        st = ''
        st = st + 'points :' + str(self.p) + '\n'
        st = st + 'fmin :' + str(self.fGHz[0]) + '\n'
        st = st + 'fmax :' + str(self.fGHz[1]) + '\n'
        return(st)

    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.p[0,:],self.p[1,:],self.p[2,:],s=20)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show()

class ULArray(Array):
    """ Uniform Linear Array

    An uniform array is centered on the origin.
    It has Nx, Ny, Nz antennas placed respectively along the x,y,z axis.


    The assumed mapping between the antenna port index ik and the spatial indexing
    (ix,iy,iz) is

    ik = iz Nx Ny + iy Nx + ix

    """
    def __init__(self,**kwargs):
        """

        Parameters
        ----------

        N  : list
            [Nx,Ny,Nz,Na]  don't use 0 the total number of antennas is Nx*Ny*Nz*Na
        dm : list of floats
            [dxm,dym,dzm] distance are expressed in meters

        """
        defaults = { 'N'    : [8,1,1,1],
                     'dm'   : [0.075,0,0,0],
                     'w'   : [],
                    'fGHz' : np.linspace(1.8,2.2,10),
                   }
        for k in defaults:
            if k not in kwargs:
                kwargs[k]=defaults[k]

        self.N  = kwargs.pop('N')
        self.dm = np.array(kwargs.pop('dm'))
        self.Na = np.prod(self.N)

        Nx = self.N[0]
        Ny = self.N[1]
        Nz = self.N[2]

        px = self.dm[0]*np.linspace(-(Nx-1)/2.,(Nx-1)/2.,Nx)[None,:,None,None] # 1 x Nx x Ny x Nz
        py = self.dm[1]*np.linspace(-(Ny-1)/2.,(Ny-1)/2.,Ny)[None,None,:,None] # 1 X Nx x Ny x Nz
        pz = self.dm[2]*np.linspace(-(Nz-1)/2.,(Nz-1)/2.,Nz)[None,None,None,:] # 1 x Nx x Ny x Nz
        #if Nx%2==0:
        #    px = self.dm[0]*np.linspace(-Nx/2,Nx/2,Nx)[None,:,None,None] # 1 x Nx x Ny x Nz
        #else:
        #    px = self.dm[0]*np.linspace(-(Nx-1)/2,(Nx-1)/2,Nx)[None,:,None,None] # 1 x Nx x Ny x Nz
        #if Ny%2==0:
        #    py = self.dm[1]*np.linspace(-Ny/2,Ny/2,Ny)[None,None,:,None] # 1 x Nx x Ny x Nz
        #else:
        #    py = self.dm[1]*np.linspace(-(Ny-1)/2,(Ny-1)/2,Ny)[None,None,:,None] # 1 X Nx x Ny x Nz
        #if Nz%2==0:
        #    pz = self.dm[2]*np.linspace(-Nz/2,Nz/2,Nz)[None,None,None,:] #  1 x Nx x Ny x Nz
        #else:
        #    pz = self.dm[2]*np.linspace(-(Nz-1)/2,(Nz-1)/2,Nz)[None,None,None,:] # 1 x Nx x Ny x Nz

        p = np.zeros((3,Nx,Ny,Nz))
        #p = np.zeros((3,Nx*Ny*Nz))

        p[0,:,:,:] = px
        p[1,:,:,:] = py
        p[2,:,:,:] = pz

        q = p.reshape((3,Nx*Ny*Nz))

        Array.__init__(self,p=q,**kwargs)

class UCArray(Array):
    """ Uniform Circular Array
    """

    pass

class AntArray(Array,ant.Antenna):
    """ Class AntArray

    inherits from Array and Antenna classes

    """

    def __init__(self,**kwargs):
        """
        Examples
        --------

        ... plot::
            :include-source:
        >>> A=AntArray()
        >>> A.plotG()

        """
        defaults = {'tarr': 'UA',
                    'N'    : [8,1,1,1],
                    'dm'   : [0.075,0,0,0],
                    'min'  : [0,0,0,0],
                    'max'  : [0,0,0,0],
                    'S'    : [],
                    'pattern' : True,
                    #'typant':'S1R1.vsh3',
                    'typant':'Gauss',
                    'mode' : 'grid'
                    }


        for k in defaults:
            if k not in kwargs:
                kwargs[k]=defaults[k]

        self.tarr = kwargs.pop('tarr')
        self.N  = np.array(kwargs.pop('N'))
        self.max  = np.array(kwargs.pop('max'))
        self.min  = np.array(kwargs.pop('min'))
        self.Na = np.prod(self.N)  # number of antennas
        self.dm = np.array(kwargs.pop('dm'))
        self.typant = kwargs.pop('typant')

        if kwargs['mode'] == 'grid':
            for  k in range(len(self.N)):
                if self.N[k]==1:
                    self.dm[k]=self.max[k]
                else:
                    self.dm[k]= (self.max[k]-self.min[k])/(self.N[k]-1.0)

        if type(self.typant)==list:
            self.sameAnt=False
            assert len(self.typant)==self.Na,"Wrong number of antennas"
        else:
            self.sameAnt=True


        if self.tarr=='UA':
           UA = ULArray(N = self.N,dm = self.dm)

        #
        # Add the antennas of the array, either 1 (same for all points), or Na
        # (array size)
        #
        typ = 'Array'
        # init Antenna parent
        self.la = []
        if self.sameAnt:
            self.la.append(ant.Antenna(typ=self.typant))
        else:
            for t in self.typant:
                self.la.append(ant.Antenna(typ=t))

        super(AntArray,self).__init__(p=UA.p,fGHz=self.la[0].fGHz)
        ant.Antenna.__init__(self,typ=typ,**kwargs)

    def __add__(self,Aa):
        assert(Aa.typant==self.typant)
        Anew = self+Aa
        Anew.typant = self.typant
        return(Anew)

    def __repr__(self):
         st = "Antenna Array : \n"
         st = st + self.typ + 'of '+self.typant+'\n'
         st = st + 'N : '+str(self.N)+'\n'
         st = st + 'dm : '+str(self.dm)+'\n'
         st = st + ant.Antenna.__repr__(self)
         return(st)


def k2xyza(ik,sh):
    """

    Parameters
    ----------

    ik : full index starting at 0
    sh : list of [Nx,Ny,Nz,Na]

    Returns
    -------

    ix , iy , iz , ia : index starting at 0


    """
    assert(len(sh)==4)
    assert(len(ik)==np.prod(np.array(sh)))

    Ny = sh[1]
    Nz = sh[2]
    Na = sh[3]

    ix = ik/(Ny*Nz*Na)
    iy = (ik-ix*Ny*Nz*Na)/(Nz*Na)
    iz = (ik-ix*Ny*Nz*Na-iy*Nz*Na)/Na
    ia = ik-ix*Ny*Nz*Na-iy*Nz*Na-iz*Na

    return(ix,iy,iz,ia)

def xyztok(iz,iy,ix,Nx=10,Ny=11):
    ik = iz*Nx*Ny+iy*Nx+ix
    return(ik)

def weights(nx,nz,kx,kz,Kx,Kz):
    """
    Practical Demonstration of Limited Feedback Beamforming for mmWave Systems

    """
    arg = np.floor((nx*np.mod(kx+(Kx/2),Kx))/(Kx/4))


if __name__=='__main__':
    doctest.testmod()
#
#
#
#
## + We assume X band
#
## In[2]:
#
## Frequency
#fGHz  = 10
## Wavelength
#lam   = 0.3/fGHz
## Wabve number
#k     = 2*pi/lam
## distance between elements
#d     = lam/2
## Number of point along thets
#Ntheta = 520
## ramp in theta
#theta = linspace(-pi/2,pi/2,Ntheta)
#thetadeg = theta* 180/pi
#
#
## In[10]:
#
## Build different set of weights
#N = 12
## n : 0,1,.....,N-1
##
#n  = arange(N)
#wu = ones(N)
#wh = hamming(N)
#wb = blackman(N)
#wc20 = si.chebwinwh = hamming(N)
#wb = blackman(N)(N,20)
#wc25 = si.chebwin(N,25)
#wc30 = si.chebwin(N,30)
#subplot(221)
#tmp=stem(n,wu)
#title('uniform')
#subplot(222)
#tmp=stem(n,wc20)
#title('Dolph-Chebyshev 20')
##title('hamming')
#subplot(223)
#tmp=stem(n,wc25)
#title('Dolph-Chebyshev 25')
#subplot(224)
#tmp=stem(n,wc30)
#title('Dolph-Chebyshev 30')
#
#
## The $N \times N_{\theta}$ steering vectors matrix is given by
##
## $$\mathbf{S}(\theta) = e^{jkd \mathbf{n}^T . \mathbf{sin(\theta)}}$$
##
## $$\mathbf{U}(\theta) = \frac{d}{d\theta}\mathbf{S}(\theta) = jkd \mathbf{n}^T.\mathbf{\cos(\theta)} \odot e^{jkd \mathbf{n}^T . \mathbf{sin(\theta)}}$$
#
## In 3D these expression becomes.
##
## Let $\mathbf{r}$ (3xN) be the coordinates associated with each element of the array.
## Let define a direction $\mathbf{\hat{s}}(\theta,\phi)$
##
## $$\mathbf{S}(\theta,\phi) = e^{-jk \mathbf{\hat{s}}^T . \mathbf{k}(\theta,\phi)}$$
#
## In[11]:
#
#u  = 1j*k*d*outer(n,sin(theta))
#v  = 1j*k*d*outer(n,cos(theta))
#S  = exp(u)
#U  = v*exp(u)
#R  = -u*exp(v)+v*v*exp(u)
#T  = S+U
#
#
## In[15]:
#
#u.shape
#
#
## In[13]:
#
#u.shape
#
#
## In[5]:
#
#^{\dagger} subplot(321)
#pcolor(thetadeg,n,real(S))
#title('Re S')
#colorbar()
#subplot(323)
#pcolor(thetadeg,n,imag(S))
#title('Im S')
#colorbar()
#subplot(325)
#colorbar()
#pcolor(thetadeg,n,angle(S))
#title('angle V')
#subplot(322)
#pcolor(thetadeg,n,real(U))
#title('Re U')
#colorbar()
#subplot(324)
#pcolor(thetadeg,n,imag(U))
#title('Im U')
#colorbar()
#subplot(326)
#colorbar()
#pcolor(thetadeg,n,angle(U))
#title('angle U')
#
#
## In[10]:
#
##J = outer(n,sin(theta))
##pcolor(thetadeg,n,J)
#
#
## In[14]:
#
#def beamwidth(FdB,theta,thresh=3):
#    Fmax = max(FdB)
#    u = nonzero(FdB>(Fmax-thresh))[0]
#    bw = theta[u[-1]]-theta[u[0]]
#    return(bw)
#
#
## In[7]:
#
#Fu  = dot(wu,S)
#Fh  = dot(wh,S)
#Fb  = dot(wb,S)
#Fc20  = dot(wc20,S)
#Fc25  = dot(wc25,S)
#Fc30  = dot(wc30,S)
#
#Fun = Fu/max(abs(Fu))
#Fhn = Fh/max(abs(Fh))
#Fbn = Fb/max(abs(Fb))
#Fcn20 = Fc20/max(abs(Fc20))
#Fcn25 = Fc25/max(abs(Fc25))
#Fcn30 = Fc30/max(abs(Fc30))
#
#FundB = 20*log10(abs(Fun))
#FhndB = 20*log10(abs(Fhn))
#FbndB = 20*log10(abs(Fbn))
#Fcn20dB = 20*log10(abs(Fcn20))
#Fcn25dB = 20*log10(abs(Fcn25))
#Fcn30dB = 20*log10(abs(Fcn30))
#Fcnmoy = (Fcn20dB+Fcn25dB+Fcn30dB)/3
#bwu = beamwidth(FundB,thetadeg)
#bwh = beamwidth(FhndB,thetadeg)
#bwb = beamwidth(FbndB,thetadeg)
#bwc20 = beamwidth(Fcn20dB,thetadeg)
#bwc25 = beamwidth(Fcn25dB,thetadeg)
#bwc30 = beamwidth(Fcn30dB,thetadeg)
#bwcmoy = beamwidth(Fcnmoy,thetadeg)
#print "beamwidth (deg) uniform : ",bwu
#print "beamwidth (deg) hamming : ",bwh
#print "beamwidth (deg) blackmann : ",bwb
#print "beamwidth (deg) Dolph-chebyshev 20: ",bwc20
#print "beamwidth (deg) Dolph-chebyshev 25: ",bwc25
#print "beamwidth (deg) Dolph-chebyshev 30: ",bwc30
#print "beamwidth (deg) Dolph-chebyshev moy: ",bwcmoy
#
#
##
#
## In[8]:
#
#plot(theta*180/pi,FundB,'b-+')
##plot(theta*180/pi,FhndB,'b-o')
##plot(theta*180/pi,FbndB,'b-*')
#plot(theta*180/pi,Fcn20dB,'r',linewidth=2)
#plot(theta*180/pi,Fcn25dB,'r-+',linewidth=2)
#plot(theta*180/pi,Fcn30dB,'r-*',linewidth=2)
#plot(theta*180/pi,Fcnmoy,'g',linewidth=3)
##legend(('uniform','hamming','blackman','Dolph-Chebyshev'))
#legend(('uniform','DC-20','DC 25','DC 30','DC averaged'))
#title('Dolph Chebyshev pattern for various rejection constraints')
#axis((-90,90,-50,0))
#xlabel('$\\theta$ (deg)')
#ylabel('dB')
#
#
##
##
## The figure above demonstates that is possible to have very small variations on the
## beamwidth while obtaining a very well controlled modulation (here more than 10dB in very stable
## direction on the sidelobes).
## This could be exploited to send a stealth amplitude modulation schemes with a symbol time $T_s$
## which could be defined as a fraction of the radar transmitting duration.
##
##
##
## Notice that the averaged pattern has exactly the same beamwidth as B-C25 but it is obviously worst regarding
## the rejection which is an expected result because Dolph-chebyschev is optimal regarding side lobe
## rejection at a specified beamwidth.
##
## + Q : Is it possible to adaptively and jointly controled the level and the direction of the sidelobes ?
##
## + Q : What is the degree of freedom we have on the modulation of the mainlobe beamwidth.
## + Q: What are the typical distances we are interested in both for communication and radar ?
##
##
## It is necessary to define a more precise radar-com scenario with associated propagation model
## in order to evaluate the difficulty of both synchronisation and data demodulation both at target
## location and intended receiver.
#
## # Finding a mathematical definition of rejection
##
## In order to expressed criteria on rejection it is important to give a precise mathematical definition of what exactly rejection is.
## Let $\mathbf{w}^T$ be the 1xN vector of antenna array weights. The complex array factor is given by :
##
## $$ \mathbf{F}(\theta)= \mathbf{w}^{\dagger} . \mathbf{S}(\theta) $$
##
## Let defines the  $N\times N $ matrix $$\mathbf{W}=\mathbf{w}^{\dagger}\mathbf{w}$$
##
## $$ |F(\theta)|^2 = \textrm{diag}(\mathbf{F}^{\dagger}(\theta)\mathbf{F})$$
## $$ |F(\theta)|^2 = \textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W} \mathbf{S} )$$
## $$ \frac{d}{d\theta}|F(\theta)|^2 = \textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{S} )+\textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W}  \mathbf{U} )$$
## $$ \frac{d^2}{d\theta^2}|F(\theta)|^2 =\textrm{diag}( \mathbf{R}^{\dagger} \mathbf{W}  \mathbf{S} )+
##                                        \textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{U} )+
##                                        \textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{U})+
##                                        \textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W}  \mathbf{R} )$$
## $$ \frac{d^2}{d\theta^2}|F(\theta)|^2 =\textrm{diag}( \mathbf{R}^{\dagger} \mathbf{W}  \mathbf{S} )+
##                                        2\textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{U} )+
##                                        \textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W}  \mathbf{R} )$$
#
## In order to expressed criteria on rejection it is important to give a precise mathematical definition of what exactly rejection is.
## Let $\mathbf{w}^T$ be the 1xN vector of antenna array weights. The complex array factor is given by :
##
## $$ \mathbf{F}(\theta,\phi)= \mathbf{w}. \mathbf{S}(\theta,\phi) $$
##
## Let defines the  $N\times N $ matrix $$\mathbf{W}=\mathbf{w}^{\dagger}\mathbf{w}$$
##
## $$ |F(\theta,\phi)|^2 = \textrm{diag}(\mathbf{F}^{\dagger}(\theta,\phi)\mathbf{F})$$
## $$ |F(\theta,\phi)|^2 = \textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W} \mathbf{S} )$$
## $$ \frac{d}{d\theta}|F(\theta)|^2 = \textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{S} )+\textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W}  \mathbf{U} )$$
## $$ \frac{d^2}{d\theta^2}|F(\theta)|^2 =\textrm{diag}( \mathbf{R}^{\dagger} \mathbf{W}  \mathbf{S} )+
##                                        \textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{U} )+
##                                        \textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{U})+
##                                        \textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W}  \mathbf{R} )$$
## $$ \frac{d^2}{d\theta^2}|F(\theta)|^2 =\textrm{diag}( \mathbf{R}^{\dagger} \mathbf{W}  \mathbf{S} )+
##                                        2\textrm{diag}( \mathbf{U}^{\dagger} \mathbf{W}  \mathbf{U} )+
##                                        \textrm{diag}( \mathbf{S}^{\dagger} \mathbf{W}  \mathbf{R} )$$
#
## In[ ]:
#
#def rejection(w,theta,fGHz=10,d=[],thresh=0.1):
#    """
#    Calculate rejection for a given arbitrary array
#
#    w     : weighting coefficient (can be complex)
#    theta : theta interval
#    fGHz  : frequency in GHz
#    d     : interelement distance (default lambda/2)
#    thresh : threshold for null first derivative evaluation
#
#    Author : B.Uguen
#             December 2011
#    """
#    N  = len(w)
#    n  = arange(N)
#    lam   = 0.3/fGHz
#    k     = 2*pi/lam
#    if d ==[]:
#        d     = lam/2
#
#    W  = outer(conj(w.T),w)
#    u  = 1j*k*d*outer(n,sin(theta))
#    v  = 1j*k*d*outer(n,cos(theta))
#    S  = exp(u)
#    U  = v*exp(u)
#    R  = -u*exp(v)+v*v*exp(u)
#    T  = S+U
#    F  = real(dot(conj(S.T),dot(W,S)))
#
#    G  = real(dot(conj(U.T),dot(W,S))+dot(conj(S.T),dot(W,U)))
#    H  = real(dot(conj(R.T),dot(W,S))+2*dot(conj(U.T),dot(W,U))+dot(conj(S.T),dot(W,R)))
#    f  = diag(F)/max(diag(F))
#    g  = diag(G)/max(diag(G))
#    h  = diag(H)/max(diag(H))
#    # max condition (first derivative absolute value below threshold and second derivative <0)
#    z1     = nonzero((abs(g)<thresh) & (h < 0))[0]
#    # find mainlobe
#    ml = nonzero((abs(f)>=0.5) & (h <0))[0]
#    # exclude mainlobe from maxima
#    z    = setdiff1d(z1,ml)
#    rejdB = log10(max(abs(f[z]))/max(abs(f)))
#    bw = theta[ml[-1]]-theta[ml[0]]
#    bwdeg = bw*180/pi
#    #print max(abs(f[z])),max(abs(f)),rejdB
#    return(f,g,h,z,ml,rejdB,bwdeg)
#
#
#def visurej(f,g,h,z,main,rejdB,bwdeg,titre1):
#    plot(thetadeg,log10(abs(f)),'k')
#    plot(thetadeg,g,'r')
#    plot(thetadeg,sign(h),'b')
#    title('Attempt to identify the sidelobes maxima : imprecise approach')
#    z     = nonzero((abs(g)<0.01) & (h < 0))[0]
#    plot(thetadeg[z],log10(abs(f[z])),'ro')
#    plot(thetadeg[main],log10(abs(f[main])),'go')
#    #rej=log10(max(abs(f[z]))/max(abs(f)))
#    axis((-90,90,-5,2))
#    legend(('F(dB)/10 ','normalized derivative (linear)','sign of 2nd der'))
#    titre = titre1+'beamwidth (deg) : '+ str(round(bwdeg*100)/100)+' achieved rejection (dB) : ' + str(round(rejdB*100)/10)
#    title(titre)
#
#
## In the figure below we have determined the locus where the absolute value is below a given threshold while the second derivative remains negative.
## This second criteria authorizes not to be very strict on the null criteria for derivative
## because on each sub-interval the function is locally convex.
#
## ## Study rejection of different arrays
#
## In[15]:
#
#Ntheta   = 500
#theta    = linspace(-pi/2,pi/2,Ntheta)
#thetadeg = theta* 180/pi
#N        = 12
#w        = ones(N)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'uniform :')
#
#
## In[16]:
#
#w        = si.chebwin(N,20)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Dolph-Chebyshev (20 dB) :')
#
#
## In[17]:
#
#w        = si.chebwin(N,25)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Dolph-Chebyshev (25dB) :')
#
#
## In[18]:
#
#w        = rand(N)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Random real 1 :')
#
#
## In[19]:
#
#w        = rand(N)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Random real 2 :')
#print rejdB
#
#
## Q: What is the mean rejection when drawing randomly a real weigthing array ? And how is it correlated to beamwidth ?
## The beamwith evaluation is imprecise because it is evaluated numerically and is dependant from the angular sampling interval.
#
## In[20]:
#
#Ntrial = 1000
#trej = []
#tbwdeg = []
#for k in range(Ntrial):
#    w        = rand(N)
#    f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#    if bwdeg >20:
#        print w
#    trej.append(rejdB*10)
#    tbwdeg.append(bwdeg)
#
#
## In[21]:
#
#tmp  = hist(trej,50)
#
#
## In[22]:
#
#hist(tbwdeg,20)
#
#
##
#
## In[23]:
#
#scatter(trej,tbwdeg)
#axis([-20,0,0,15])
#
#
## In[24]:
#
#w        = rand(N)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Random real 3 :')
#
#
##
#
## In[9]:
#
#w.w        = rand(N)+1j*rand(N)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Random complex 1 :')
#
#
## In[26]:
#
#w        = rand(N)+1j*rand(N)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Random complex 2 :')
#
#
## In[27]:
#
#w        = blackman(N)+1j*blackman(N)
#f,g,h,z,main,rejdB,bwdeg = rejection(w,theta)
#visurej(f,g,h,z,main,rejdB,bwdeg,'Complex : ')
#
#
## ## Definition of an averaged radiation pattern
##
## The averaged radiation pattern is defined as :
##
## $$ \mathbf{\bar{F}}(\theta)=\frac{1}{K}\sum_{k=1}^{K} \mathbf{F}_k(\theta)= \frac{1}{K}\sum_{k=1}^{K} \mathbf{w_k}^{\dagger} . \mathbf{S}(\theta) $$
#
## If we assume a weight encoded with $N_b$ bits, $\mathbf{u_k}$ is equal to 0 or 1
##
## $$\mathbf{w_k} = \mathbf{u_k}(2^{N_b}-1) $$
#
## $$ \mathbf{\bar{F}}_K(\theta) = \frac{2^{N_b}-1}{K}\sum_{k=1}^{K} \mathbf{u_k}^{\dagger} . \mathbf{S}(\theta) $$
#
## $$N_{bit} = \log_2 \left( K (2^{N_b}-1) +1\right) $$
#
## Time modulated array
##
## $$ \mathbf{F}(\theta,t)=\sum_{l=-\infty}^{+\infty} \textrm{rect}(\frac{t- l T/2}{T})\mathbf{F}_l(\theta) $$
##
#
##
## Time modulated array
##
## $$ \mathbf{\bar{F}}(\theta) = \frac{1}{K}\sum_{k=1}^{K} \mathbf{w_k}^{\dagger} . \mathbf{S}(\theta) $$
#
## Nombre d'antennes constant  Hopt
#
## $$ \frac{1}{KT}\int_{0}^{K T}  \mathbf{F}(\theta,u) du $$
##
## $$  \frac{1}{KT}\sum_{l=-\infty}^{+\infty} \mathbf{F}_l(\theta) \int_{0}^{K T}\textrm{rect}(\frac{t- l T/2}{T}) dt   $$
##
#
## $$ \mathbf{\bar{F}}_{K}(\theta) = \sum_{l=1}^{K} \mathbf{F}_l(\theta)   $$
#
## Time modulated array
##
## $$ \mathbf{F}(\theta,t)=\frac{1}{K}\sum_{k=1}^{K} \textrm{rect}(\frac{t- l T_k/2)}{T_k})\mathbf{F}_k(\theta)= \frac{1}{K}\sum_{k=1}^{K} \mathbf{w_k}^{\dagger} . \mathbf{S}(\theta) $$
#
## Interfrence Radar
#
##  ## POSTMA
#
#el(dot(conj(U.T),dot(W,S))+dot(conj(S.T),dot(W,U)))
#    H  =
#    real(dot(conj(R.T),dot(W,S))+2*dot(conj(U.T),dot(W,U))+dot(conj(S.T),dot(W,R)))# Comparaison petit rseau et grand rseau.
