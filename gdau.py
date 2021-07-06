#!/usr/bin/env python
# coding: utf-8
# Version with command line arguments
import os
import time
import argparse
import glob
import shutil
from pathlib import Path
#from tkinter import filedialog
#from tkinter import *
import datetime
import urllib.request
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size
def statbar(current, max_img, max_res = 100, sign = "|", flank = "<>", empty = " "):
    progress = int((current/max_img)*max_res)
    remaining = int((1-(current/max_img))*max_res)
    print(f"{flank}{sign*progress}{empty*remaining}{flank}")
parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, required = True)
parser.add_argument("--drone", type=str, required = True)
parser.add_argument("--path", type=str, required = True)
parser.add_argument("--counterres", type = int, default = 5)
args = parser.parse_args()
counter_resolution = 1
#date = input('Date of flight? (yyyy-mm-dd)\n')
date = args.date
year, month, day = date.split('-')
isValidDate = True
try:
    datetime.datetime(int(year), int(month), int(day))
except ValueError:
    isValidDate = False
if not isValidDate:
    quit()
#drone = input('Which drone? P4M, P4RGB or Micasense?\n')
drone = args.drone
destination = Path("//largefile.nmbu.no/Project/V-Pheno/Raw_images/2021")
if drone in ['P4M', 'P4RGB', 'Micasense']:
    destination = os.path.join(destination, drone)
    print('Drone recognized...\n')
else:
    print('Invalid drone!\n')
    quit()

#path_test = filedialog.askdirectory(title = 'Select image directory')
path_test = args.path
directories = glob.glob(os.path.join(path_test, '*'))

expected_folders = ['graminor_cal', 'graminor_images',
                   'masbasis_cal', 'masbasis_images',
                   'nobalyield_cal', 'nobalyield_images',
                   'robot_cal', 'robot_images',
                   'nobalnue_cal', 'nobalnue_images']
actual_folders = []
for field in expected_folders:
    if os.path.join(path_test, field) in directories:
        actual_folders.append(os.path.join(path_test, field))
print(str(len(actual_folders)), end = '')
print(' folders found in the directory...\n')
temp = []
for field_path in actual_folders:
    temp.append(os.path.basename(os.path.normpath(field_path)).split('_')[0])
temp = list(dict.fromkeys(temp))
# Check if the directory exists already!
#to_path = os.path.join(destination, field, date)
for field in temp:
    #itr = 1
    #while os.path.isdir(to_path):
        #to_path = os.path.join(to_path, "_", itr)
        #itr += 1
    os.mkdir(os.path.join(destination, field, date))
    if not drone == 'Micasense':
        os.mkdir(os.path.join(destination, field, date, 'RGB'))
        os.mkdir(os.path.join(destination, field, date, 'RGB', 'images'))
        os.mkdir(os.path.join(destination, field, date, 'RGB', 'cal'))
    if (drone == 'P4M') or (drone == 'Micasense'):
        os.mkdir(os.path.join(destination, field, date, 'Multispectral'))
        os.mkdir(os.path.join(destination, field, date, 'Multispectral', 'images'))
        os.mkdir(os.path.join(destination, field, date, 'Multispectral', 'cal'))
print('Directories created!\n')
# Generate raport of upload
raport = open(os.path.join(destination,'upload_raports',(date + '_' + drone + "_" + "_".join(temp) + "_upload_raport.txt")),"w")
raport.write("::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
raport.write("::::::::::UPLOAD RAPORT OF IMAGES TO LARGEFILE::::::::::\n")
raport.write("::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
data_format = "%d/%m/%Y %H:%M:%S"
raport.write(f"Raport created on: {datetime.datetime.now().strftime(data_format)}\n")
raport.write("Summary of user input:\n")
raport.write(f"\tFlight date:\t{date}\n")
raport.write(f"\tDrone:\t{drone}\n")
raport.write(f"\tUpload source:\t{path_test}\n")
raport.write(f"Total directory size:\t{round(get_size(path_test)/1048576, ndigits=2)} Mb\n")
raport.write(f"Target path:\t{destination}\n")
raport.write(f"Number of fields provided:\t{str(len(temp))}\n")
raport.write("Folders provided and number of photos:\n")
for field in temp:
    field_dirs = [dir for dir in actual_folders if field in dir]
    raport.write(f"\t{field}:\n")
    raport.write(f"\t\tcal:\t{str(len(os.listdir(field_dirs[0])))}")
    raport.write(f"\t\timages:\t{str(len(os.listdir(field_dirs[1])))}")
    raport.write(f"\tsum:{str(len(os.listdir(field_dirs[0])) + len(os.listdir(field_dirs[1])))}\n")
total_sum = 0
for field in temp:
    field_dirs = [dir for dir in actual_folders if field in dir]
    for subfield in field_dirs:
        total_sum = total_sum + len(os.listdir(subfield))
raport.write(f"Total number of images:\t{str(total_sum)}\n")
raport.write("Internet status:\t")
raport.write("Connected\n" if connect() else "No connection, aborting...\n")
raport.write(f"LargeFile available:\t{str(os.path.isdir(destination))}\n")
raport.write(f"Upload started:\t{datetime.datetime.now().strftime(data_format)}\n")
raport.write('Detailed upload progress:\n')
start_time = datetime.datetime.now()
print('Raport opened!\n')
print('Starting upload!\n')
time.sleep(4)
# for P4RGB
if drone == 'P4RGB':
    counter = 0
    for field in temp:
        field_dirs = [dir for dir in actual_folders if field in dir]
        raport.write(f"{datetime.datetime.now().strftime(data_format)}\tCopying images for field:\t{field}\n")
        for source_dir in field_dirs:
            files_to_transfer = os.listdir(source_dir)
            if '_cal' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'RGB', 'cal')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto:\t{target_path}\n")
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{str(round(counter*100/total_sum))} % done\n")
                        print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                        statbar(counter, total_sum)
            if '_images' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'RGB', 'images')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto: {target_path}\n")
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{str(round(counter*100/total_sum))} % done\n")
                        print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                        statbar(counter, total_sum)
# for Micasense
if drone == 'Micasense':
    counter = 0
    for field in temp:
        field_dirs = [dir for dir in actual_folders if field in dir]
        raport.write(f"{datetime.datetime.now().strftime(data_format)}\tCopying images for field:\t{field}\n")
        for source_dir in field_dirs:
            files_to_transfer = os.listdir(source_dir)
            if '_cal' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'Multispectral', 'cal')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto:\t{target_path}\n")
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{str(round(counter*100/total_sum))} % done\n")
                        print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                        statbar(counter, total_sum)
            if '_images' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'Multispectral','images')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto:\t{target_path}\n")
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{str(round(counter*100/total_sum))} % done\n")
                        print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                        statbar(counter, total_sum)
if drone == 'P4M':
    counter = 0
    for field in temp:
        field_dirs = [dir for dir in actual_folders if field in dir]
        raport.write(f"{datetime.datetime.now().strftime(data_format)}\tCopying images for field:\t{field}\n")
        for source_dir in field_dirs:
            files_to_transfer = os.listdir(source_dir)
            if '_cal' in source_dir:
                for file in files_to_transfer:
                    if ('.JPG' in file) or ('.jpg' in file):
                        target_path = os.path.join(destination, field, date, 'RGB', 'cal')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto:\t{target_path}\n")
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"{str(round(counter*100/total_sum))} % done\n")
                            print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                            statbar(counter, total_sum)
                    if ('.TIF' in file) or ('.tif' in file):
                        target_path = os.path.join(destination, field, date, 'Multispectral', 'cal')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto:\t{target_path}\n")
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"{str(round(counter*100/total_sum))} % done\n")
                            print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                            statbar(counter, total_sum)
            if '_images' in source_dir:
                for file in files_to_transfer:
                    if ('.JPG' in file) or ('.jpg' in file):
                        target_path = os.path.join(destination, field, date, 'RGB', 'images')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto:\t{target_path}\n")
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"{str(round(counter*100/total_sum))} % done\n")
                            print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                            statbar(counter, total_sum)
                    if ('.TIF' in file) or ('.tif' in file):
                        target_path = os.path.join(destination, field, date, 'Multispectral', 'images')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(f"{datetime.datetime.now().strftime(data_format)}\tFile: {file}\tto:\t{target_path}\n")
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"{str(round(counter*100/total_sum))} % done\n")
                            print(f"Time remaining: [hh-mm-ss-ms] {estimated}\t {str(progress_time)} per file\n")
                            statbar(counter, total_sum)
end_time = datetime.datetime.now()
duration = end_time - start_time
raport.write(f"Upload finished at: {datetime.datetime.now().strftime(data_format)}\nTotal images uploaded: {str(counter)}\nTime elapsed: {str(duration)}")
raport.close()



