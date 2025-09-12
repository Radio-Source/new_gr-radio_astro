# new_gr-radio_astro
DSPIRA spectro radiometer modified code Work on Ubuntu 24.04 LTS or Windows 10-11 
---
![new_gr-radio_astro_spectrometer](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/using3_new_gr-radio_astro_spectrometer.png)

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

Download and install Python 3.12 or 3.13 https://www.python.org/downloads/windows/

Use CMD console to install Qt5 with command :
```bash
pip3 install pyqt5
```
Download and install radioconda (Gnuradio for Windows) https://github.com/ryanvolz/radioconda

Read comment about SDR install under Windows

Download git for easy copying my repository  https://git-scm.com/downloads/win
After install open CMD shell and goto your Documents directory
Then type command :
```bash
git clone https://github.com/Radio-Source/new_gr-radio_astro/
```
![new_gr-radio_astro_cmd-git](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_cmd-git.png)

to copy my new_gr-radio_astro repository in your Documents directory

Now goto Documents/new_gr-radio_astro repository for the next step to install
![new_gr-radio_astro_dir](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_dir.png)

copy radioconda sub directory into c:
--------------------------------
radioconda/Lib/ra_funcs    (Python file)

radioconda/Lib/site-packages/gnuradio/radio_astro/      (Python files)

radioconda/Library/share/gnuradio/grc/blocs/     (yml files)


![new_gr-radio_astro_nuradio_dir](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_nuradio_dir.png)

Restart Windows ^^
---------------

Open radioconda (Gnuradio) 
![new_gr-radio_astro-gnuradio-windows](https://github.com/user-attachments/assets/71c6853b-a6ff-4c70-903d-71fdf8691530)

In file menu goto /Documents/new_gr-radio_astro/DSPIRA/ directory and open
 "spectrometer_w_cal_new.grc"
then run flowgraph

------------------------------------------------------------------------------------------------

![new_gr-radio_astro_flow_graph](https://github.com/user-attachments/assets/26bf04c3-c633-4173-9dc5-967a31670dfb)

You can change some parameters in flowgraph (see explanation in the Docs of DSPIRA)

for example, if you whant to go up the power from our SDR to lna, change in osmocom source Bias value 0 to 1
airpy=0,bias=1,pack=0

In my original flowgraph have remover SDR value for using with all SDR hardware.

![new_gr-radio_astro_edit_flowgraph](https://github.com/user-attachments/assets/881a64fe-53ab-4ace-9ecf-889b87d032de)


