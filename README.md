SURE poster: [YZhang.pdf](https://github.com/user-attachments/files/16791334/YZhang.pdf)

Report for SURE Project:

1.	Pump set up

The pump needs to be set up for two parameters, pressure and flow rate. The percentage of pressure and flow rate on pump interface can be interpreted into manometric unit, mmHg and metric unit, mL/min. The parameter reference tables are shown below. 

1.1 Set up for pressure parameter testing conditions

The default pulse rate is 72 bpm and the duration of high pressure is 100 ms. 
The error of every 10% change is ±15 mmHg. Due to the pulsation effect of the pump, the pressure measured above is the average value of the pulsation cycle per unit time (10 s) at the output of the portable pulsation pump, which is for reference only. The pressure value measured in the model will be slightly smaller than the pressure value at the output end, and the actual pressure value is subject to your actual measurement. 
The set flow value of the pump determines the lower limit of output pressure (minimum pressure per stroke), and the pressure setting determines the upper limit of output pressure (maximum pressure per stroke). The high-pressure duration controls the duration of the maximum pressure value of the output; the pulse rate does not affect the maximum and minimum pressure values of the output end, but only affects the speed of its change.
<img width="433" alt="image" src="https://github.com/user-attachments/assets/5f528262-9e38-4ece-b99b-1c21fdff39a6">

Fig 1. Reference table of pressure parameter

1.2 Set up for flow rate parameter testing conditions

Error range: The error of every 10% change is ±15 mmHg. Due to the pulsation effect of the pump, the flow value measured above is the average value of the pulsation cycle per unit time (10s) at the output of the portable pulsation pump, which is for reference only. The flow value measured in the blood vessel model will be slightly smaller than the flow value at the output end, and the actual flow value is subject to your actual measurement).
The pump’s flow setting value determines the lower limit of the output flow (minimum flow per stroke), and the pressure setting determines the upper limit of the output flow (the maximum flow per stroke). The high-pressure duration controls the duration of the maximum flow value of the output; the change of pulse rate will slightly affect the flow value of the output end, when pulse rate is increased by 20 bpm per time, the flow value will be increased by 0.03 L/min. 

<img width="416" alt="image" src="https://github.com/user-attachments/assets/7d4925e7-8d2f-4c2f-b82f-96d26d0178b5">

Fig 2. Reference table of flow parameter

 
2.	Arduino and python interface set up
Due to the unfunctional grove base shield, the flow sensor is test one by one. The setup of flow sensor and servo motor is shown below. The flow sensor is directly connected to Elegoo UNO R3 panel (Uno panel). The black wire connected with GND, red wire connected with 3V3, and white wire connects with digital pin 2. The servo motors are connected to the Adafruit 16 channel servo driver as the original set up. The DC power supply is set to 7.4 V. (The link for the spec sheet of YF-S401 flow sensor).
The code for Arduino and python interface can be found in main respiratory. 

 <img width="468" alt="image" src="https://github.com/user-attachments/assets/27efccfc-1b34-4290-bb81-96d7619229ce">

Fig 3. Arduino set up for flow sensor testing


3.	Devices for future studies

For the originally used Grove Based Shield, the Arduino PIN numbers, and grove connector numbers are shown in the figure 4 below. 
<img width="415" alt="zzzzz" src="https://github.com/user-attachments/assets/ebe4c675-4862-4a99-87bc-eb7842c09a67">
Fig 4. The interface of 

For the originally used Grove Based Shield, the Arduino PIN numbers, and grove connector numbers are shown in the figure 4 below.

<img width="336" alt="image" src="https://github.com/user-attachments/assets/0c76a786-43a2-4f2f-9b7d-967823f2691e">

Fig 5. The interface of grove base shield
In figure 5, the interface of grove base shield  
 
Fig x. The detailed 

