import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
n_customer=int(input("Enter number of customers:"))
n_grids=int(input("Enter the number of grids:"))
energy_init=int(input("Enter EV Energy(units):"))
grid_val=float(input("Enter the grid revenue per unit:"))
random.seed(1);np.random.seed(1)
depot=(50,50)
customer=[tuple(np.random.randint(10,90,2)) for _ in range(n_customer)]
grid=[tuple(np.random.randint(10,90,2)) for _ in range(n_grids)]
location=[depot]+customer+grid
colors=['red']+['green']*n_customer+['blue']*n_grids
distance=lambda p,q:np.hypot(p[0]-q[0],p[1]-q[1])
def routing_plan(depot,customer,grid,energy,pay_per_unit):
    path,current,used=[depot],depot,0
    unvisited_cust=customer[:]
    while unvisited_cust:
        next = min(unvisited_cust, key=lambda j: distance(current, j))
        if used + distance(current, next) > energy: break
        used += distance(current, next)
        path.append(next); current = next; unvisited_cust.remove(next)

    reminder=energy-sum(distance(path[i],path[i+1])for i in range(len(path)-1))
    best,profit=None,-1
    for k in grid:
            to_grid ,to_depot=distance(current,k),distance(k,depot)
            if reminder >=to_grid+to_depot:
                discharge=reminder-to_depot
                a=discharge*pay_per_unit
                if a>profit:
                    best,profit=k,a
    if best:
          path.append(best);current=best
    path.append(depot)
    total=sum(distance(path[i],path[i+1])for i in range (len(path)-1))
    energy_left=max(0,energy-total)
    return path,profit,energy_left
path,pay,energy_final=routing_plan(depot,customer,grid,energy_init,grid_val)
fig,ax=plt.subplots(figsize=(8,8))
ax.set(xlim=(0,100),ylim=(0,100),title="Ev Routing",xlabel="x",ylabel="y")
ax.grid(True)
for i ,loc in enumerate(location):
    ax.plot(*loc,'o',color=colors[i])
    label="Depot" if i==0 else f'C{i}' if i<=n_customer else f'G{i-n_customer}'
    ax.text(loc[0]+1, loc[1]+1, label, fontsize=8)
def interplation(path,step=20):
    return[(x1+t*(x2-x1),y1+t*(y2-y1))
           for (x1,y1),(x2,y2) in zip(path,path[1:])
           for t in np.linspace(0,1,step)]+[path[-1]]
smooth=interplation(path)
lines,=ax.plot([],[],'y-',lw=2)
dots,=ax.plot([],[],'yo',markersize=8)
txt=ax.text(2,95,'',fontsize=10,bbox=dict(facecolor='white'))
final_text=ax.text(2,5,'',fontsize=10,bbox=dict(facecolor='white'),visible=False)
xdata,ydata=[],[]
def init():
    lines.set_data([],[])
    dots.set_data([],[])
    txt.set_text('')
    final_text.set_visible(False)
    return lines,dots,txt,final_text
def update(frame):
    x,y=smooth[frame]
    xdata.append(x);ydata.append(y)
    lines.set_data(xdata,ydata)
    dots.set_data([x],[y])
    c=sum(distance(smooth[i],smooth[i+1])for i in range(frame))
    energy_val=max(0,100*(energy_init-c)/energy_init)
    show_pay=any(distance((x,y),k)<2 for k in grid)
    txt.set_text(f"Energy:{energy_val:.1f}%{'  |  ₹'+str(round(pay,1)) if show_pay else ''}")
    if frame==len(smooth)-1:
        final_text.set_text(f"Final Energy:{energy_final/energy_init*100:.1f}%\nTotal Revenue: ₹{pay:.1f}")
        final_text.set_visible(True)
    return lines,dots,txt,final_text
anime=animation.FuncAnimation(fig,update,frames=len(smooth),init_func=init,interval=60,blit=True,repeat=False)
plt.show()