import os 
    

def check_folder_size(path):


    byte_to_gb = 1e+9       #fomula byte to gb
    img_size = 0
    count_remove = 0

    img_size = 0
    # get size
    for ele in os.scandir(path):
        img_size+=os.stat(ele).st_size      #size in byte

    img_size_in_gb = img_size/byte_to_gb
    # print("byte : ", img_size, "byte")
    print("Total images   : ", round(img_size_in_gb,2), "GB")

def count_total_file_in_folder(path):
    count_file = 0
    for files in os.listdir(path):
        count_file +=1
    print(f'Total file is {count_file}')
        
        
if __name__ == '__main__':

    path = '/home/delloyd/9.coding'
    
    check_folder_size(path)
    count_total_file_in_folder(path)
    
    

        

        

