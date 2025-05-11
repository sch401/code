import os
import re

def rename_files_in_directory(directory):
    # 遍历当前目录及所有子目录
    for root, _, files in os.walk(directory):
        for file in files:
            # 分离文件名和扩展名
            base_name, ext = os.path.splitext(file)
            
            # 检查文件名是否符合模式：以 "(1)" 或 "（2）" 结尾，且括号前有空格
            match = re.match(r'^(.+)\s+[\(\（][1-9][\)\）]$', base_name)
            if match:
                # 提取去掉括号和空格后的文件名
                new_base_name = match.group(1)
                new_file_name = new_base_name + ext
                
                # 构造完整路径
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_file_name)
                
                # 检查新文件名是否已存在
                if not os.path.exists(new_path):
                    print(f'Renaming: {old_path} -> {new_path}')
                    os.rename(old_path, new_path)
                else:
                    print(f'Skipping: {old_path} (conflict with existing file)')

if __name__ == "__main__":
    # 当前文件夹路径
    current_directory = os.getcwd()
    
    # 执行重命名操作
    rename_files_in_directory(current_directory)
