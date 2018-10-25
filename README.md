# BDD100K2VOC2012
Python codes to transfer the labels of BDD100K with json format to xml format of VOC2012

json_extract.py extracts the information that are needed by the VOC format from the original BDD labels
    edit the variable PATH_TO_JSON to be the directory where you stored the .json file of BDD100K

json2xml.py reads the information from the extracted json file and transfer the information into xml format, each picture corresponds to one xml file
    edit the file_path (line 59) to where you stored the pictures of BDD100K
    
