# new_gr-radio_astro
DSPIRA spectro radiometer modified code Work on Ubuntu 24.04 LTS or Windows 10-11 
---
![new_gr-radio_astro_spectrometer](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/using3_new_gr-radio_astro_spectrometer.png)

Summary
-------------

* Prerequisites

* Linux Install

* Windows 10-11 install

* Usage


----------------------------------------------------------------------------------------------------------------------------------------------------

Prerequisites
-------------

Python 3.xx
GnuRadio (linux)
Radioconda (Windows)

----------------------------------------------------------------------------------------------------------------------------------------------------




Linux Install 
-------------
(please see explainations here https://github.com/WVURAIL/gr-radio_astro or in my fork https://github.com/Radio-Source/gr-radio_astro

Then copy or clone my modified code of DSPIRA Spectrometer in https://github.com/Radio-Source/new_gr-radio_astro/tree/main/DSPIRA

Run Gnuradio-Compagnion open /DSPIRA/spectrometer_w_cal_new.grc and run 
Next you run directly from shell with command :
Python3 DSPIRA_Spectrometer.py


----------------------------------------------------------------------------------------------------------------------------------------------------

Windows 10-11 install
---------------------
1st ! you have and SDR working on your computer with dedicated software, like sdrsharp for example !

Download and install Python 3.12 or 3.13 https://www.python.org/downloads/windows/

Use CMD console to install Qt5 with command :
```bash
pip3 install pyqt5
```
Download and install radioconda (Gnuradio for Windows)  (install for user only not for all) 
https://github.com/ryanvolz/radioconda

Read comment about SDR install under Windows

Download git for easy copying my repository  https://git-scm.com/downloads/win
After install open CMD shell and goto your Documents directory
Then type command :
```bash
cd Documents
git clone https://github.com/Radio-Source/new_gr-radio_astro/
```
![new_gr-radio_astro_cmd-git](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_cmd-git.png)

Open Files Browser, to copy my new_gr-radio_astro repository in your Documents directory

Goto Documents/new_gr-radio_astro repository for the next step to install
![new_gr-radio_astro_dir](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_dir.png)

copy radioconda sub directory into c:\ProgramData\
--------------------------------

this copies these folders into c:\ProgramData\radioconda\

radioconda\Lib\ra_funcs    (Python file)

radioconda\Lib\site-packages\gnuradio\radio_astro\      (Python files)

radioconda\Library\share\gnuradio\grc\blocs\     (yml files)


![new_gr-radio_astro_nuradio_dir](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_nuradio_dir.png)

Don't miss Restart Windows ^^
---------------

----------------------------------------------------------------------------------------------------------------------------------------------------

Usage
---------------

Open radioconda software (Gnuradio) 
![new_gr-radio_astro-gnuradio-windows](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro-gnuradio-windows.png)

If you have Airspy
---------------

In file menu goto \Documents\new_gr-radio_astro\DSPIRA\ directory and open flowgraph
 "spectrometer_AIRSPY_new.grc"

------------------------------------------------------------------------------------------------

![new_gr-radio_astro_flow_graph](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_flow_graph_AIRSPY.png)

You can change some parameters in flowgraph by double click on the box

for example, if you whant to go up integrated Airspy BiasTee to lna (eg: Nooelec SHAWbird H1), change in osmocom source Bias **value 0 to 1**, by default is bias=0
```bash
airpy=0,bias=1,pack=0
```

![using_new_gr-radio_astro-AIRSPY_biastee_parameters](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/using_new_gr-radio_astro-AIRSPY_biastee_parameters.png)

If you have other SDR
---------------

In file menu goto \Documents\new_gr-radio_astro\DSPIRA\ directory and open flowgraph
 "spectrometer_SDR_new.grc"


![new_gr-radio_astro_flow_graph_SDR](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/new_gr-radio_astro_flow_graph_SDR.png)

You can change these parameters for all SDR type
---------------

Sampling rate
---------------

For Airspy R2 is 10e6(10 Mhz) or 2.5e6 (2.5 Mhz) for Airspy Mini is 6e6 (6 Mhz) or 2.5e6 (2.5 Mhz)

By defaut is 10 Mhz in AIRSPY flowgraph because I have AIrspy R2 and have best result with these value.

For other SDR by default the value is a common value 2.5e6 (2.5 Mhz), you can change as you whant.

![using_new_gr-radio_astro-samp_rate](https://github.com/Radio-Source/new_gr-radio_astro/blob/main/img/using_new_gr-radio_astro-samp_rate.png)

----------------------------------------------------------------------------------------------------------------------------------------------------

Astronomical parameters
---------------

These parameters are used to calculate the sidereal time and the observed declination
Used in the name of the file for simplify data post processing.

You can change by double click on the box or while the software running :
Location (QT GUI ENTRY Location)
AMSL (QT GUI ENTRY amsl - Altitude Above Mean Sea Level in meters)


Contributing
---------------

NSF (National Science Foundation) DSPIRA (Digital Signal Processing in Radio Astronomy)

https://wvurail.org/dspira/

ra_funcs python code from Marcus Leech Canadian Centre for Experimental Radio Astronomy

https://www.ccera.ca/about/


