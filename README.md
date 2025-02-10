# new_gr-radio_astro
DSPIRA spectro radiometer modified code 
 
Work on Ubuntu 24.04 LTS or Windows 10-11 
-----------------------------------------
prerequisites
Python 3.xx
GnuRadio (linux)       Radioconda (Windows)
----------------------------------------------------------------------------------------------------------------------------------------------------
Linux Install (please see explainations here https://github.com/WVURAIL/gr-radio_astro or in my fork https://github.com/Radio-Source/gr-radio_astro
-------------
Then copy or clone my mofified code of DSPIRA Spectrometer in https://github.com/Radio-Source/new_gr-radio_astro/tree/main/DSPIRA

Run Gnuradio-Compagnion open /DSPIRA/spectrometer_w_cal.grc and run 
Next you run directly from shell with command :
Python3 DSPIRA_Spectrometer.py


Windows 10-11
-------------
Download and install Python 3.12 https://www.python.org/downloads/windows/
Download and install radioconda (Gnuradio for Windows) https://github.com/ryanvolz/radioconda
Download git for easy copying my repository
After install open CMD shell and goto your Documents directory
Then type command : git clone https://github.com/Radio-Source/new_gr-radio_astro/
![new_gr-radio_astro_cmd-git](https://github.com/user-attachments/assets/311a77b3-4a9e-498c-ad65-43ce8cca50d9)

to copy my new_gr-radio_astro repository in your Documents directory
Now goto Documents/new_gr-radio_astro repository for the next step to install
![new_gr-radio_astro_dir](https://github.com/user-attachments/assets/13f28fff-2901-468f-8a72-c66e3cc770ba)

copy inside radioconda directory 
--------------------------------
radioconda/Lib/site-packages/radio_astro/      (Python files)

radioconda/Library/share/gnuradio/grc/blocs/     (yml files)

Restart Windows ^^
---------------

Open radioconda (Gnuradio) 
![new_gr-radio_astro-gnuradio-windows](https://github.com/user-attachments/assets/71c6853b-a6ff-4c70-903d-71fdf8691530)

In file menu got /Documents/new_gr-radio_astro/DSPIRA/ directory and open "spectrometer_w_cal.grc" then run
------------------------------------------------------------------------------------------------


