#!/usr/bin/env python
# coding: utf-8

import os
import time
import argparse
import glob
import shutil
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import datetime
import urllib.request
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

counter_resolution = 5
date = input('Date of flight? (yyyy-mm-dd)\n')
year, month, day = date.split('-')
isValidDate = True
try:
    datetime.datetime(int(year), int(month), int(day))
except ValueError:
    isValidDate = False
if not isValidDate:
    quit()
drone = input('Which drone? P4M, P4RGB or Micasense?\n')
destination = Path("//largefile.nmbu.no/Project/V-Pheno/Raw_images/2021/")
if drone in ['P4M', 'P4RGB', 'Micasense']:
    destination = os.path.join(destination, drone)
    print('Drone recognized...\n')
else:
    print('Invalid drone!\n')
    quit()

path_test = filedialog.askdirectory(title = 'Select image directory')
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
for field in temp:
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
raport = open(os.path.join(destination, 'upload_raports', (date + '_' + drone + "_upload_raport.txt")), "w")
raport.write("::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
raport.write("::::::::::UPLOAD RAPORT OF IMAGES TO LARGEFILE::::::::::\n")
raport.write("::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
raport.write("Raport created on:                   ")
raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
raport.write("\n")
raport.write("Summary of user input:\n")
raport.write("Flight date:                                  ")
raport.write(date)
raport.write("\n")
raport.write("Drone:                                             ")
raport.write(drone)
raport.write("\n")
raport.write("Chosen topmost upload directory:\n")
raport.write(path_test)
raport.write("\n")
raport.write("Target path:\n")
raport.write(destination)
raport.write("\n")
raport.write("Number of fields provided:                             ")
raport.write(str(len(temp)))
raport.write("\n")
raport.write("Folders provided and number of photos:\n")
for field in temp:
    field_dirs = [dir for dir in actual_folders if field in dir]
    raport.write("  ")
    raport.write(field)
    raport.write("\n")
    raport.write('    cal: ')
    raport.write(str(len(os.listdir(field_dirs[0]))))
    raport.write("\timages: ")
    raport.write(str(len(os.listdir(field_dirs[1]))))
    raport.write("\tsum: ")
    raport.write(str(len(os.listdir(field_dirs[0])) + len(os.listdir(field_dirs[1]))))
    raport.write('\n')
total_sum = 0
for field in temp:
    field_dirs = [dir for dir in actual_folders if field in dir]
    for subfield in field_dirs:
        total_sum = total_sum + len(os.listdir(subfield))
raport.write('Total number of images:\t')
raport.write(str(total_sum))
raport.write('\n')
raport.write("Internet status:\t")
raport.write( "Connected\n" if connect() else "No connection, aborting...\n")
raport.write('LargeFile available:\t')
raport.write(str(os.path.isdir(destination)))
raport.write('\n')
raport.write("Upload started:\t")
raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
raport.write('\n')
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
        raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        raport.write('\tCopying images for field: ')
        raport.write(field)
        raport.write('\n')
        #print('Copying images for field: ')
        #print(field)
        #print('\n')
        #print('Copying file: \n')
        for source_dir in field_dirs:
            files_to_transfer = os.listdir(source_dir)
            if '_cal' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'RGB', 'cal')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    raport.write('\tFile: ')
                    raport.write(file)
                    raport.write('\tto:\n')
                    raport.write(target_path)
                    raport.write('\n')
                    #print(file)
                    #print('                                                          ')
                    #print('\r')
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(str(round(counter*100/total_sum)), end = '')
                        print('% done\n')
                        #print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
                        print('Estimated time until completion: [hh-mm-ss-ms]\t')
                        print(estimated)
                        print("\t")
                        print(str(progress_time))
                        print(" per file\n")
            if '_images' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'RGB', 'images')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    raport.write('\tFile: ')
                    raport.write(file)
                    raport.write('\tto:\n')
                    raport.write(target_path)
                    raport.write('\n')
                    #print(file)
                    #print('                                                          ')
                    #print('\r')
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(str(round(counter*100/total_sum)), end = '')
                        print('% done\n')
                        print('Estimated time until completion: [hh-mm-ss-ms]\t')
                        print(estimated)
                        print("\t")
                        print(str(progress_time))
                        print(" per file\n")
# for Micasense
if drone == 'Micasense':
    counter = 0
    for field in temp:
        field_dirs = [dir for dir in actual_folders if field in dir]
        raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        raport.write('\tCopying images for field: ')
        raport.write(field)
        raport.write('\n')
        #print('Copying images for field: ')
        #print(field)
        #print('\n')
        #print('Copying file: \n')
        for source_dir in field_dirs:
            files_to_transfer = os.listdir(source_dir)
            if '_cal' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'Multispectral', 'cal')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    raport.write('\tFile: ')
                    raport.write(file)
                    raport.write('\tto:\n')
                    raport.write(target_path)
                    raport.write('\n')
                    #print(file)
                    #print('                                                          ')
                    #print('\r')
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(str(round(counter*100/total_sum)), end = '')
                        print('% done\n')
                        #print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')
                        print('Estimated time until completion: [hh-mm-ss-ms]\t')
                        print(estimated)
                        print("\t")
                        print(str(progress_time))
                        print(" per file\n")
            if '_images' in source_dir:
                for file in files_to_transfer:
                    target_path = os.path.join(destination, field, date, 'Multispectral','images')
                    file = os.path.join(source_dir, file)
                    shutil.copy(file, target_path)
                    counter = counter + 1
                    raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    raport.write('\tFile: ')
                    raport.write(file)
                    raport.write('\tto:\n')
                    raport.write(target_path)
                    raport.write('\n')
                    #print(file)
                    #print('                                                          ')
                    #print('\r')
                    if counter % counter_resolution == 0:
                        progress_time = (datetime.datetime.now() - start_time)/counter
                        estimated = (total_sum - counter)*progress_time
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(str(round(counter*100/total_sum)), end = '')
                        print('% done\n')
                        print('Estimated time until completion: [hh-mm-ss-ms]\t')
                        print(estimated)
                        print("\t")
                        print(str(progress_time))
                        print(" per file\n")

if drone == 'P4M':
    counter = 0
    for field in temp:
        field_dirs = [dir for dir in actual_folders if field in dir]
        raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        raport.write('\tCopying images for field: ')
        raport.write(field)
        raport.write('\n')
        #print('Copying images for field: ')
        #print(field)
        #print('\n')
        #print('Copying file: \n')
        for source_dir in field_dirs:
            files_to_transfer = os.listdir(source_dir)
            if '_cal' in source_dir:
                for file in files_to_transfer:
                    if ('.JPG' in file) or ('.jpg' in file):
                        target_path = os.path.join(destination, field, date, 'RGB', 'cal')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        raport.write('\tFile: ')
                        raport.write(file)
                        raport.write('\tto:\n')
                        raport.write(target_path)
                        raport.write('\n')
                        #print(file)
                        #print('                                                          ')
                        #print('\r')
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(str(round(counter*100/total_sum)), end = '')
                            print('% done\n')
                            print('Estimated time until completion: [hh-mm-ss-ms]\t')
                            print(estimated)
                            print("\t")
                            print(str(progress_time))
                            print(" per file\n")
                    if ('.TIF' in file) or ('.tif' in file):
                        target_path = os.path.join(destination, field, date, 'Multispectral', 'cal')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        raport.write('\tFile: ')
                        raport.write(file)
                        raport.write('\tto:\n')
                        raport.write(target_path)
                        raport.write('\n')
                        #print(file)
                        #print('                                                          ')
                        #print('\r')
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(str(round(counter*100/total_sum)), end = '')
                            print('% done\n')
                            print('Estimated time until completion: [hh-mm-ss-ms]\t')
                            print(estimated)
                            print("\t")
                            print(str(progress_time))
                            print(" per file\n")
            if '_images' in source_dir:
                for file in files_to_transfer:
                    if ('.JPG' in file) or ('.jpg' in file):
                        target_path = os.path.join(destination, field, date, 'RGB', 'images')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        raport.write('\tFile: ')
                        raport.write(file)
                        raport.write('\tto:\n')
                        raport.write(target_path)
                        raport.write('\n')
                        #print(file)
                        #print('                                                          ')
                        #print('\r')
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(str(round(counter*100/total_sum)), end = '')
                            print('% done\n')
                            print('Estimated time until completion: [hh-mm-ss-ms]\t')
                            print(estimated)
                            print("\t")
                            print(str(progress_time))
                            print(" per file\n")
                    if ('.TIF' in file) or ('.tif' in file):
                        target_path = os.path.join(destination, field, date, 'Multispectral', 'images')
                        file = os.path.join(source_dir, file)
                        shutil.copy(file, target_path)
                        counter = counter + 1
                        raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        raport.write('\tFile: ')
                        raport.write(file)
                        raport.write('\tto:\n')
                        raport.write(target_path)
                        raport.write('\n')
                        #print(file)
                        #print('                                                          ')
                        #print('\r')
                        if counter % counter_resolution == 0:
                            progress_time = (datetime.datetime.now() - start_time)/counter
                            estimated = (total_sum - counter)*progress_time
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(str(round(counter*100/total_sum)), end = '')
                            print('% done\n')
                            print('Estimated time until completion: [hh-mm-ss-ms]\t')
                            print(estimated)
                            print("\t")
                            print(str(progress_time))
                            print(" per file\n")


raport.write("Upload finished at: ")
raport.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
end_time = datetime.datetime.now()
raport.write('\nTotal images uploaded: ')
raport.write(str(counter))
raport.write("\nTime elapsed: ")
duration=end_time - start_time
raport.write(str(duration))
raport.close()




