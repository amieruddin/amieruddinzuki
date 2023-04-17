from itertools import count
import os
from re import S
import shutil
from humanize import naturalsize
import time


# src = '/home/delloyd/9.coding/delete_file_more_than_3_monts/full/archive'
# src = '/home/delloyd/9.coding/delete_file_more_than_3_monts/crop'                 #2.4gb
# src = "/media/delloyd/6072266F72264A5C/ANPR_DATA_CHECKING/z.combine/train/images"   #4.4gb
# src = "/media/delloyd/6072266F72264A5C/outstation/data_collection_v3/Kuantan"       #5.2gb
src = "/media/delloyd/6072266F72264A5C/data_collection_v2/gombak/full"              #70.9gb

src_kingston = "/media/delloyd/VAVC_KESAS_1/Data_collection_v3_Gombak-Jabur_September/testing_for_delete"

current_folder = src.split("/")[-1] #get last path


def get_dir_size_shutil_disk():

    path = src_kingston

    limit_size = 50.0
    count=1

    total_memory_size = naturalsize(shutil.disk_usage(src_kingston).total)
    size_use = shutil.disk_usage(src_kingston).used     #get memory use in HD | .used @ .total @ .free
    size = naturalsize(size_use, format='%.1f')         #converted into GB
    print("\n* Hard Disk    | ",path.split("/")[3])
    print(f"* Total memory |  {total_memory_size}")
    print(f"* Current use  |  {size}")
    print("\n")
    
    
    #delete file
    size_memory = float(size.split(" ")[0])

    if size_memory > limit_size:   
        
        dir = sorted(os.listdir(path)) #list all img in folder
        filename = [x.split(".")[0] for x in dir]  #filter date into list
        # print("filename\n",filename, "\n")

        print("*** [Removing old file] ***")
        for y in os.listdir(path):
            if y[0:8] == filename[0]:
                filename_path = os.path.join(path, y)
                # print(filename_path)
                # os.remove(filename_path)
                print(count, y)
                count+=1
        print(f"\n*** {count-1} files have been remove ")
        print("*** Summary after clean up ")
        size_use = shutil.disk_usage(src_kingston).used     #get memory use in HD | .used @ .total @ .free
        size_summary = naturalsize(size_use, format='%.1f')         #converted into GB
        print("\n* Hard Disk        | ",path.split("/")[3])
        print(f"* Total memory     |  {total_memory_size}")
        print(f"* Current memory   |  {size_summary}")
        cleaning = float(size_summary.split(" ")[0])
        cleaning = size_memory - cleaning
        print(f"* Memory clean     |  {round(cleaning,1)} GB")
        print("\n")
    
    else:
        print("*** Still have memory for save img")
    

if __name__ == "__main__":

    start_time = time.time()

    get_dir_size_shutil_disk() 


    print("\n--- %s seconds ---" % round((time.time() - start_time),3))

