# XRD23D - 3D Visulaization of XRD measurements

---

Standalone programs to combine files from XRD measurements with a given location to plot in 3D (see **DOI_OF_PUBLICATION** for more details)

---

# Instructions

Follow instructions to combine multiple .csv files with XRD measurements and associate a location to each measurement point to be able to plot the measurements in 3D

---
### Step 1 – Prepare Input

- Prepare __folder__ with .csv files with XRD measurements
  - .csv files have to have __";"__ as delimiter
  - Data Points have to start after a row called __Angle;Intensity__
- Prepare __.csv file__ with location of each measurment
  - ID for each measurement have to be __exactly__ as the XRD measurement file naming
    - Example: Sample ID might be abc1234 -> XRD file has to be named abc1234.csv
  - You could prepare an file in excel and go to "Save As..." and select CSV as file format


### Step 2 - Download executable program

- Git clone or download respository to your personal computer (green button in the upper right corner)
- Go to __XRD23D/executables__ and exectute either the *win* or the *unix* (also mac) program depening on your machine by double-click
  - You could also run the python script from the __python__ folder
- An terminal window will open with Instructions
  - 1. Select __folder__ with .csv files with XRD measurements
    - *You might not see files on a windows machine, don't get confused ;-)*
  - 2. Select __.csv file__ with location of each measurement
  - 3. Select __folder__ where to save the combined file
    - File will be called combined_xrd_3d.csv
    - xrd23d.log file contains further information and error messages
- Wait a second an check the terminal window for more information or potential errors
- Press any key to close
