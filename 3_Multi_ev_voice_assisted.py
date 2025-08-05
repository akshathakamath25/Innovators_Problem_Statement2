import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.animation as animation
import math,random,os
from datetime import datetime
import pyttsx3
def audio(text):
     try:
          engine=pyttsx3.init()
          engine.setProperty('rate',165)
          engine.setProperty('volume',1.0)
          voices=engine.getProperty('voices')
          engine.setProperty('voice', voices[0].id)
          engine.say(text)
          engine.runAndWait()
     except:
          print("[Error in Voice]")
def dist(p,q):
        return math.hypot(p['x']-q['x'],p['y']-q['y'])
def is_peak():
        hour=datetime.now().hour
        return(10<=hour<12) or (18<=hour<20)
def rating(peak,off):
        return peak if is_peak() else off
def loading_data(f_path):
        df=pd.read_csv(f_path)
        df.columns=df.columns.str.strip().str.replace('.', '', regex=False)
        depot = {'x': df.iloc[0]['XCOORD'], 'y': df.iloc[0]['YCOORD']}
        df = df.iloc[1:].copy()
        df['x'] = df['XCOORD']
        df['y'] = df['YCOORD']
        return depot,df.reset_index(drop=True)
def route_plan(depot,customer,grids,energy,rate):
    STOCK=0.22
    SUPPLY=0.3
    rem_energy=energy
    path=[depot.copy()]
    pay=0
    for _,m in customer.iterrows():
        a={'x':m['x'],'y':m['y']}
        b= dist(path[-1],a)
        if rem_energy<b+energy*STOCK:break
        path.append(a)
        rem_energy-=b
    end=path[-1]
    grid=min(grids,key=lambda g:dist(end,g))
    if rem_energy>=dist(end,grid)+dist(grid,depot)+energy*STOCK:
        path.append(grid)
        rem_energy-=dist(end,grid)
        dis=min(rem_energy-dist(grid,depot)-energy*STOCK,energy*SUPPLY)
        pay+=max(0,dis)*rate
        rem_energy-=dis
    path.append(depot.copy())
    return path,pay

def animating(paths,depot,customer,grids,energy):
    global all_pos,dots,trails,texts
    fig,ax=plt.subplots(figsize=(9,7))
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    colors=plt.cm.tab10.colors
    dots,trails,texts=[],[],[]
    all_pos=[]
    for k in paths:
        points,rem=[],energy
        for i in range(len(k)-1):
            p,q=k[i],k[i+1]
            b=dist(p,q)
            step=20
            for j in np.linspace(0,1,step):
                x=p['x']+j*(q['x']-p['x'])
                y=p['y']+j*(q['y']-p['y'])
                rem-=b/step
                points.append((x,y,max(0,rem/energy*100)))
        all_pos.append(points)
    for i ,_ in enumerate(paths):
        dot,=ax.plot([], [], 'o', color=colors[i], label=f'EV-{i+1}')
        trail,=ax.plot([], [], '-', lw=2, color=colors[i])
        txt=ax.text(0,0,'',fontsize=9)
        dots.append(dot)
        trails.append(trail)
        texts.append(txt)
    ax.scatter(customer['x'],customer['y'],c='green',marker='x',label='Customers')
    ax.scatter(depot['x'],depot['y'],c='red',s=101,label='Depot')
    for i,g in enumerate(grids):
        ax.scatter(g['x'],g['y'],c='yellow',marker='s',s=101)
        ax.text(g['x']+1,g['y']+1,f"G{i+1}",color='yellow',fontsize=10)
    ax.set_title("Multiple Ev Routing")
    ax.legend()
    anime=animation.FuncAnimation(fig,update,frames=max(len(a) for a in all_pos),
                                  interval=100,blit=True,repeat=False)
    plt.tight_layout()
    plt.show()

def update(frame):
        for i,position in enumerate(all_pos):
            if frame<len(position):
                if frame < len(position):
                 xs, ys, socs = zip(*position[:frame+1])
                 trails[i].set_data(xs, ys)
                 dots[i].set_data([xs[-1]], [ys[-1]])
                 texts[i].set_position((xs[-1] + 1, ys[-1] + 1))
                 texts[i].set_text(f"SoC: {socs[-1]:.1f}%")
        return dots + trails + texts

def main():
     audio("Multiple Ev Routing")
     f_path=input("Enter dataset path:").strip()
     if not os.path.exists(f_path):
          print("File not Found")
          audio("File not found...retry")
          return
     depot,customer=loading_data(f_path)
     ev=int(input("Number of Evs:"))
     grids=int(input("Number of Grid stations:"))
     energy=int(input("Initial Energy/Charge:"))
     peak = float(input("Peak ₹/unit: "))
     off= float(input("Off-peak ₹/unit: "))
     animate_flags = input("Show animation? (y/n): ").lower() == 'y'

     rate=rating(peak,off)
     duration="peak" if is_peak() else "off_peak"
     print(f"{duration.capitalize()} hour rate: ₹{rate}")
     audio(f"{duration.capitalize()} hour detected. Using rate {rate} per unit.")

     kmeans = KMeans(n_clusters=ev, random_state=0)
     customer['cluster'] = kmeans.fit_predict(customer[['x', 'y']])
     grid_station = [{'x': random.uniform(10, 90), 'y': random.uniform(10, 90)} for _ in range(grids)]

     all_route, all_revenue = [],[]
     for i in range(ev):
        cluster_customer = customer[customer['cluster'] == i]
        route, revenue = route_plan(depot, cluster_customer, grid_station,energy, rate)
        all_route.append(route)
        all_revenue.append(revenue)
        print(f"EV-{i+1} → Revenue: ₹{revenue:.1f}")

     total_rev = sum(all_revenue)
     print(f"💰 Total Revenue: ₹{total_rev:.1f}")
     audio(f"Simulation complete. Total revenue is ₹{total_rev:.1f}")

     if animate_flags:
        audio("Starting animation.")
        animating(all_route, depot, customer, grid_station, energy)

if __name__ == "__main__":
    main()



    
    
    
