import os
import shutil

# 当前目录

def photoclassification(start,common_difference):
    current_directory = '.'
    # 遍历当前目录下的所有子文件夹
    dir_path = []
    for root, dirs, files in os.walk(current_directory):
        for dir in dirs:
            # 打印子文件夹路径
            dir_name = os.path.join(root, dir)
            dir_path.append(dir_name)
    print(dir_path)
    for j in range(len(dir_path)):

        print(dir_path[j])
        # 源文件夹路径
        source_folder = dir_path[j]
        print(source_folder)
        # 目标文件夹根路径
        destination_root = dir_path[j]
        print(destination_root)


        # 等差数列的起始值和公差
        # 获取源文件夹中所有的.JPG文件
        jpg_files = [file for file in os.listdir(source_folder) if file.lower().endswith('.jpg')]
        jpg_files.sort()  # 按文件名从小到大排序
        foldernumer = len(jpg_files)//5
        abondon = len(jpg_files)%5
        jpg_files = jpg_files[abondon:]
        # 创建目标文件夹并将文件复制到对应文件夹中
        for i, jpg_file in enumerate(jpg_files):
            destination_folder_index = start + (i // 5) * common_difference
            destination_folder = os.path.join(destination_root, str(destination_folder_index))

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            source_file_path = os.path.join(source_folder, jpg_file)
            destination_file_path = os.path.join(destination_folder, jpg_file)
            shutil.move(source_file_path, destination_file_path)

if __name__ =="__main__":
    import sys
    photoclassification(sys.argv[1],sys.argv[2])
    print("文件整理完成！")

