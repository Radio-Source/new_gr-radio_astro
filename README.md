# new_gr-radio_astro
DSPIRA spectro radiometer modified code Work on Ubuntu 24.04 LTS or Windows 10-11 
---
![new_gr-radio_astro_spectrometer](https://github.com/user-attachments/assets/c0ef4436-4f04-4f5e-8d5d-d5c68c0e4ca6)

 
prerequisites
Python 3.xx
GnuRadio (linux)       Radioconda (Windows)
----------------------------------------------------------------------------------------------------------------------------------------------------




Linux Install (please see explainations here https://github.com/WVURAIL/gr-radio_astro or in my fork https://github.com/Radio-Source/gr-radio_astro
-------------
Then copy or clone my modified code of DSPIRA Spectrometer in https://github.com/Radio-Source/new_gr-radio_astro/tree/main/DSPIRA

Run Gnuradio-Compagnion open /DSPIRA/spectrometer_w_cal.grc and run 
Next you run directly from shell with command :
Python3 DSPIRA_Spectrometer.py






Windows 10-11 install
---------------------
1st ! you have and SDR working on your computer with dedicated software, like sdrsharp for example !

Download and install Python 3.12 https://www.python.org/downloads/windows/

Download and install radioconda (Gnuradio for Windows) https://github.com/ryanvolz/radioconda

Read comment about SDR install under Windows

Download git for easy copying my repository
After install open CMD shell and goto your Documents directory
Then type command :

git clone https://github.com/Radio-Source/new_gr-radio_astro/
![new_gr-radio_astro_cmd-git](https://github.com/user-attachments/assets/311a77b3-4a9e-498c-ad65-43ce8cca50d9)

to copy my new_gr-radio_astro repository in your Documents directory

Now goto Documents/new_gr-radio_astro repository for the next step to install
![new_gr-radio_astro_dir](https://github.com/user-attachments/assets/13f28fff-2901-468f-8a72-c66e3cc770ba)

copy inside radioconda directory (radioconda dir is inside your user namespace)
--------------------------------
radioconda/Lib/site-packages/gnuradio/radio_astro/      (Python files)

radioconda/Library/share/gnuradio/grc/blocs/     (yml files)

Restart Windows ^^
---------------

Open radioconda (Gnuradio) 
![new_gr-radio_astro-gnuradio-windows](https://github.com/user-attachments/assets/71c6853b-a6ff-4c70-903d-71fdf8691530)

In file menu goto /Documents/new_gr-radio_astro/DSPIRA/ directory and open "spectrometer_w_cal.grc" then run
------------------------------------------------------------------------------------------------

![new_gr-radio_astro_flow_graph](https://github.com/user-attachments/assets/26bf04c3-c633-4173-9dc5-967a31670dfb)

