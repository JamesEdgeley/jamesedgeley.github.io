import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
from matplotlib.widgets import Slider


class lattice:
    def __init__(self,nrow,ncol):
        self.data = np.where(np.random.random((nrow, ncol)) > 0.5, 1, -1)
        self.energ=self.energy(0,0)

    def deltaE(self,i,j,J,H):
        rows,cols = self.data.shape
        adj=self.data[i,(j+1)%cols]+self.data[i,(j-1)%cols]+self.data[(i+1)%rows,j]+self.data[(i-1)%rows,j]
        return 2*self.data[i,j]*(J*adj+H)
        
    def step(self,i,j,J,H,T):
        dE=self.deltaE(i,j,J,H)
        p=np.random.random()
        if dE<0 or (T!=0 and np.exp((-dE)/T))>p:
            self.energ+=dE
            self.data[i,j] = -self.data[i,j]

    def stepN(self,N,J,H,T):
        rng = np.random.default_rng()
        rands=rng.integers(0,[self.data.shape],size=(N,2))
        for k in range(N):
            i,j=rands[k]
            self.step(i,j,J,H,T)

    def energy(self, J, H):
        rows,cols = self.data.shape
        energy=0
        for i in range(rows):
            for j in range(cols):
                adj=self.data[i,(j+1)%cols]+self.data[i,(j-1)%cols]+self.data[(i+1)%rows,j]+self.data[(i-1)%rows,j]
                energy-=self.data[i,j]*(J*adj+H)
        return energy/4



def run(rows=256,cols=256):
    fig,(ax,ax2,ax3,ax4,ax5)= plt.subplots(5, 1,figsize=(10,10), height_ratios=[5, 1, 1, 1, 1])
    fig.subplots_adjust(bottom=0.3)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax2.set_xlim(0,1000)
    ax2.set_ylim(-5,5)
    ax3.set_xlim(0,1000)
    ax3.set_ylim(0,100)
    ax4.set_xlim(0,1000)
    ax4.set_ylim(-10,10)
    ax5.set_xlim(0,1000)
    ax5.set_ylim(-5,5)
    cmap = colors.ListedColormap(['white', 'red'])
    ax_H = plt.axes([0.05, 0.05, 0.9, 0.03])
    ax_T = plt.axes([0.05, 0.10, 0.9, 0.03])
    ax_J = plt.axes([0.05, 0.15, 0.9, 0.03])
    s_H = Slider(ax_H, r'H', -5, 5, valinit=0, valstep=0.2)
    s_T = Slider(ax_T, r'T', 0, 100, valinit=10, valstep=2)
    s_J = Slider(ax_J, r'J', -10, 10, valinit=0, valstep=0.2)

    N=rows*cols//50
    latt=lattice(rows,cols)
    J,H,T=0,0,1
    heatmap = ax.imshow(latt.data,cmap=cmap,vmin=-1,vmax=1, animated=True)
    xdata=[]
    y2data=[]
    y3data=[]
    y4data=[]
    y5data=[]
    line2,=ax2.plot([],[])
    line3,=ax3.plot([],[])
    line4,=ax4.plot([],[])
    line5,=ax5.plot([],[])

    plots=[heatmap,line2,line3,line4,line5]
    def update(t):
        H=s_H.val
        T=s_T.val
        J=s_J.val
        if(t%1000==0 and t>=500):
            ax2.set_xlim(t,t+1000)
            ax3.set_xlim(t,t+1000)
            ax4.set_xlim(t,t+1000)
            ax5.set_xlim(t,t+1000)

        latt.stepN(N,J,H,T)
        heatmap.set_data(latt.data)
        xdata.append(t)
        y2data.append(H)
        y3data.append(T)
        y4data.append(J)
        y5data.append(latt.energ/(rows*cols))
        line2.set_data(xdata,y2data)
        line3.set_data(xdata,y3data)
        line4.set_data(xdata,y4data)
        line5.set_data(xdata,y5data)
        return plots

    def updateH(t):
        H=s_H.val
        latt.energ=latt.energy(J,H)

    def updateT(t):
        T=s_T.val

    def updateJ(t):
        J=s_J.val
        latt.energ=latt.energy(J,H)


    s_H.on_changed(updateH)
    s_T.on_changed(updateT)
    s_J.on_changed(updateJ)
    ani = animation.FuncAnimation(fig, update, interval=1,blit=True)
    plt.show()


if __name__=="__main__":
    run()