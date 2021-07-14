For directory generation and automatic file upload to largefile.

The script is tailored to field season 2021, for other seasons it has to be altered.
It is designed to work as a command-line tool - either cmd or Anaconda prompt. 
Before you start! Make sure Python is added to your PATH, if not, then you have to 
point the interpreter instead of just writing "Python". If you have Anaconda Prompt, 
use it, it will make life easier.

How the script works:
1. It scans a directory given in --path argument for FOLDERS with names:
  masbasis_cal
  masbasis_images
  graminor_cal
  graminor_images
  robot_cal
  robot_images
  nobalnue_cal
  nobalnue_images
  nobalyield_cal
  nobalyield_images
  NB! Make sure there are no typo's when you create those directories, otherwise they
  won't be uploaded!
  _cal folders contain calibration images, _images contain... images.
  --path is the topmost directory containing all the directories for the fields.
  Example: 
  Your card looks like this: 
   D:\DCIM\graminor_cal
          \graminor_images
          \masbasis_cal
          \masbasis_images
          \robot_cal
          \robot_images
  So your --path argument should liik like: --path "D:\DCIM"
2. Creates necessary directories:

  /Raw_images/2021/$Drone/$Field/$Date/Multispectral
                                                    /cal
                                                    /images
                                      /RGB          
                                                    /cal
                                                    /images
  Directory structure is defined by the --drone. Micasense has only Multispectral, 
  P4RGB has only RGB and P4M has both.
  $Drone is the input to --drone argument. Can be one of: P4M, P4RGB or Micasense.
  $Date is the input to --date. HAS TO BE IN YYYY-MM-DD format!
  $Field is what is indicated by folders specified in --path. It will create these
  directories for each field present in --path. 
3.Uploads all the images on a one-by-one basis and sorts them in the process (JPGs and TIFs).
4.Generates report with all the details. Report folder can be found in:
  /Raw_images/2021/P4M
                  /Micasense
                  /P4RGB
  NB! It is hidden!

Practical quick-start:
Launch Anaconda Prompt and type:
python gdau\gdau.py --date "2000-01-01" --drone "Micasense" --path "D:\DCIM"
Done!
If you want to run multiple cards/folders:
Create a plain text file and save it as .bat
Inside it put your commands on a line-by line basis.
Open Anaconda prompt and execute the .bat file.
Good luck!

