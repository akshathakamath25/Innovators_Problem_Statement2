# EV Routing With Multi-Service Delivery Model

This repository provides Python scripts for solving the Electric Vehicle(EV) Routing Problem with Multi-Service Delivery Model,considering delivery of goods to all the customers and discharging energy to the grid during peak hours for additional revenue.

# Project Structure

|- '1_Single_ev.py'       # Simulates EV routing for a single EV with user-defined customer and grid locations.
|- '2_Multiple_ev.py'     # Simulates EV routing for multiple EVs using Solomon VPR Dataset.
|- '3_Multi_ev_voice_assisted.py'      # Simulates multi-EV routing using Solomon VRP dataset, supports voice feedback, and visualizes energy usage and grid interactions.

## Features and Functionality

### 1) 1_Single_ev.py
Input: Number of customers, grid stations, EV energy capacity, grid unit rate

Routing:
* Visits customers based on shortest path
* If energy remains, visits grid station to discharge

Visualization:
- Depot: Red
- Customers: Green
- Grid Stations: Blue
- EV: Yellow
- Animated path showing energy usage and revenue collection

### 2) 2_Multiple_ev.py
Dataset-based Routing using Solomon VRP CSV files
Input:Number of customers, grids, EVs, energy level, and revenue per unit

Routing:
* Customers are divided among EVs
* Each EV independently plans its route

Visualization:
- Unique color for each EV path
- Summary of final energy and revenue per EV

### 3) 3_Multi_ev_voice_assisted.py
Dataset-based Routing using Solomon VRP CSV files

Input:
- File path of dataset (first point = depot, rest = customers)
- Number of EVs and grid stations
- Initial energy and peak/off-peak grid revenue

Features:
* Voice feedback on status, revenue, and events
* KMeans clustering to assign customers per EV
* Visual animation of each EV’s delivery and energy discharge path

Visualization:
- Depot: Red
- Customers: Green
- Grid Stations: Yellow squares
- EVs: Moving colored dots with SoC(Source of Charge) display

## Technology Stack
- Python 3.x
- Pandas, NumPy
- Matplotlib (with animation)
- Scikit-learn (for KMeans clustering)
- pyttsx3 (for offline voice assistant)

## Routing Logic
- Customer visits: Shortest distance first while maintaining energy threshold
- Grid discharge:
  * Only if energy is sufficient to return to depot
  * Discharges only a portion of energy (0.3 max), keeping enough to return
- Revenue:
Energy sent to grid × current rate (peak/off-peak)

## Future Advancements
- Real-Time GPS Tracking
- Connect to Live Order & Grid Data
- Onboard EV Units for Battery Monitoring











