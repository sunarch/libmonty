
import requests
import shutil


x_start  = -703
x_finish = -694

z_start  = -506
z_finish = -500


def download_tile(arg_x, arg_z):
    
    url = "https://dynmap.avalion.hu/tiles/world/flat/-22_-16/{x}_{z}.png".format(x=arg_x, z=arg_z)
    path = "tiles-download-py/{x}_{z}.png".format(x=arg_x, z=arg_z)
    
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as target_file:
            for data_chunk in response:
                target_file.write(data_chunk)


for iter_x in range(x_start, x_finish + 1):
    print("------------------------------------------")
    print("iteration for x = {x}".format(x=iter_x))
    
    for iter_z in range(z_start, z_finish + 1):
        print("    instance z = {z}".format(z=iter_z))
        print("        -22_-16/{x}_{z}.png".format(x=iter_x, z=iter_z))
        
        download_tile(iter_x, iter_z)

