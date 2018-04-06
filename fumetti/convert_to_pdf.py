import os
import img2pdf
import sys

for root, dirs, files in os.walk("immagini"):
    path = root.split(os.sep)
    path_str = os.sep.join(path)
    os.rename(path_str, path_str.replace(" ", "_"))

    if len(path) > 1:  # sei in una subfolder
        pdf_name = path[1]
        file_list = []

        for file in files:
            newfile = file.zfill(10)
            fullpath_str1 = os.sep.join(path + [file])
            fullpath_str2 = os.sep.join(path + [newfile])
            os.rename(fullpath_str1, fullpath_str2)
            file_list.append(fullpath_str2)

        file_list.sort()
        pdf_path = os.path.join('pdf', '{}.pdf'.format(pdf_name))
        os.system("convert " + ' '.join(file_list) + ' ' + pdf_path)
