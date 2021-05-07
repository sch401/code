import os
path = 'e:/2'
os.chdir(path)
old_dir=os.listdir(path)
print("原始目录为 %s"%old_dir)
for file in old_dir:
    name = file.replace(" ","")
    #print(name[0:8])
    if name[0:8] == "Comments":
        print(name[8:-5])
        new_rename = name[8:-5]+" Comments"+".docx"
        os.rename(file,new_rename)
    else:
        print("ok")

