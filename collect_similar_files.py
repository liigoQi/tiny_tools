import os 
import shutil

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

father_path = '/Users/qiyifan/Downloads/'
target_path = '/Users/qiyifan/Downloads/collected/'
mkdir(target_path)

# 搜集目标文件路径
found_dirs = []
for root, dirs, files in os.walk(father_path, topdown=False):
    #print('现在的目录：', root)
    #print('目录下的文件：', files)
    if len(files) == 1 and '.lrtemplate' in files[0]:
        file_dir = root + '/' + files[0]
        found_dirs.append(file_dir)
print(found_dirs)

for dir in found_dirs:
    fpath, fname = os.path.split(dir)
    print(fname)
    shutil.copy(dir, target_path + fname)

