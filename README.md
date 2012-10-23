GroundWave Online Simulator
=========
![Mou icon](http://blog.sciencenet.cn/upload/blog/images/2010/1/2010131192831148.JPG)

## Overview

The aim of this project is to accomplish an **online simulation system** based on ns-2 open source network simulator to **simulate advanced high frequency (HF) network**.

In this project, the online simulation system should ask for the configuration parameters of the transmitter and receiver radio station within an **Online Graphical User Interface (GUI)**, and bring back the result to the user. 

For the development of this project, it uses **New Zealand conductivity database**, **a high-resolution elevation dataset (Google Map API)**.

 To calculate the **field strength** and **basic path loss** due to ground wave propagation, this project choose to **use ITU GRWAVE** program.


### Usage
	Need to be complete


### Team Member
Adam Czerniejewski

Si Chen

### Features
1. Suit the method of calculation to the ITU-R P.368-9 for groundwave field strength.
2. Include topographical data.
3. Include conductivity maps to be able to process the coverage under one area and fields profiles automatically.
4. Extend the GRWAVE to calculate the field strength with different terrain conductivity. 
5. Create an easy-to-use graphical user interface to simplify the methods described at ITU-R Rec
6. Use ns-2 to prepared and executes a network model by using Shadowing Model. (The result include throughput and delay and the simulation trace file).
7. Create a B/S system to allow user run simulation and get the result online.
8. Use Google Map API to achieve data visualization.
9. Use MySQL Database to store simulation data


### Future Work
This project could be expanded in several ways:
1. Implement Cognitive Radio Cognitive Network Simulator (CRCN) into ns-2
2. Implement Google Map Weather Service to add real-time weather data as a parameter into current simulation system.
3. Provide more accurate geographic data and support other countries.
4. Give simulation feedback and node deploy advice.
5. Support multi-pair-nodes and show the interference between them.
6. Support simulate HF ground wave propagation over saltwater and sea ice.

