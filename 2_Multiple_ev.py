import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np,random,math
n_customer=int(input("Enter the number of customers:"))
n_grid=int(input("Enter the number of grids:"))
n_ev=int(input("Enter number of EVs:"))
ev_energy=int(input("Enter thr Ev starting Energy(1000=100%):"))
grid_rev=float(input("Revenue per unit:"))
random.seed(42);np.random.seed(42)
depot=(50,50)
distance=lambda p,q:math.hypot(p[0]-q[0],p[1]-q[1])
customer=[(random.randint(10,90),random.randint(10,90)) for _ in range(n_customer)]
grid=[(random.randint(10,90),random.randint(10,90)) for _ in range(n_grid)]
customer_assigning=lambda customers,f:[customers[i::f] for i in range(f)]
assigning=customer_assigning(customer,n_ev)

def route_planning(depot,customers,grid,energy,rate):
    path,pay,trace=[depot],0.0,[0.0]
    current,used,remainder=depot,0.0,set()
    for k in customers[:]:
        d=distance(current,k)
        if used+d+distance(k,depot)>energy:break
        path.append(k);used+=d;current=k;trace.append(pay)
    rem_energy=energy-used
    while True:
        best=max(((h,rem_energy-distance(current,h)-distance(h,depot))
                  for h in grid if h not in remainder and rem_energy> distance(current,h)+distance(h,depot)),
                  key=lambda x:x[1],default=(None,-1))
        
        if best[1]<=0:break
        h=best[0];d=distance(current,h)
        rem_energy-=d;current=h;path.append(h)
        pay+=best[1]*rate;rem_energy=distance(h,depot);trace.append(pay);remainder.add(h)
    if current!=depot:path.append(depot);trace.append(pay)
    return path,pay,trace
paths,pays,traces=[],[],[]
for m in assigning:
    s,rev,t=route_planning(depot,m,grid,ev_energy,grid_rev)
    paths.append(s);pays.append(rev);traces.append(t)
def interpolating(path,step=20):
    return[(x1 + t*(x2 - x1), y1 + t*(y2 - y1))
            for (x1, y1), (x2, y2) in zip(path, path[1:])
            for t in np.linspace(0, 1, step)] + [path[-1]]
smooth=[interpolating(s) for s in paths]
max_frame=max(len(s) for s in smooth)
fig,ax=plt.subplots(figsize=(8,8))
ax.set(xlim=(0,100),ylim=(0,100),title="Ev routing with user input", xlabel="x",ylabel="y")
ax.grid(True)
ax.scatter(*depot,color='red');ax.text(*depot,"Depot",color='red')
for i,k in enumerate(customer):ax.scatter(*k,color='green');ax.text(*k,f'k{i+1}',color='green')
for l,h  in enumerate(grid):ax.scatter(*h,color='blue');ax.text(*h,f'h{l+1}',color='blue')
colors=plt.cm.tab10.colors
line=[ax.plot([],[],'-',lw=2, color=colors[i])[0] for i in range(n_ev)]
dot = [ax.plot([], [], 'o', color=colors[i])[0] for i in range(n_ev)]
label = [ax.text(2, 95 - i * 5, '', color=colors[i]) for i in range(n_ev)]
summary = ax.text(2, 2, '', fontsize=10, bbox=dict(facecolor='white'), visible=False)
xdata, ydata = [[] for _ in range(n_ev)], [[] for _ in range(n_ev)]
final_energy, final_pay = [0]*n_ev, [0]*n_ev

def init():
    for n,d,r in zip(line,dot,label):n.set_data([],[]);d.set_data([],[]);r.set_text('')
    summary.set_visible(False)
    return line+dot+label+[summary]

def update(frames):
    for i in range(n_ev):
        if frames<len(smooth[i]):
            x,y=smooth[i][frames]
            xdata[i].append(x); ydata[i].append(y)
            line[i].set_data(xdata[i], ydata[i]); dot[i].set_data([x], [y])
            energy_left = max(0, ev_energy - sum(distance(smooth[i][l], smooth[i][l+1]) for l in range(min(frames, len(smooth[i]) - 1))))
            rev_pay = traces[i][min(frames // 20, len(traces[i]) - 1)]
            final_energy[i], final_pay[i] = energy_left, rev_pay
            label[i].set_text(f"EV-{i+1} SoC: {energy_left:.1f}, ₹{rev_pay:.1f}")
    if frames == max_frame - 1:
        summary.set_text("FINAL SUMMARY:\n" + "\n".join([f"EV-{i+1}: SoC={final_energy[i]:.1f}, ₹{final_pay[i]:.1f}" for i in range(n_ev)]))
        summary.set_visible(True)
    return line + dot + label + [summary]

ani = animation.FuncAnimation(fig, update, frames=max_frame, init_func=init,
                              interval=100, blit=True, repeat=False)
plt.show()