import xml.etree.ElementTree as ET
import json
import os
from skimage import io, data

# 美化xml文件
def prettyXml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作


x1 = []
y1 = []
x2 = []
y2 = []
classname = []
truncate = []
occlude = []
# 读取json里的内容,allData表示整个.json的内容，data表示遍历的当前元素
with open("outputall.json", "r+") as f:
    allData = json.load(f)
    # data = allData["annotations"]
    print("read ready")

#####################此步骤将每一个图片的全部信息读为img_all列表的一个元素
one_img = []
img_all = []
j = 0

for i in range(1, len(allData)):
    if allData[i]['filename']==allData[i-1]['filename']:
        one_img.append(allData[i-1])
    else:
        j += 1
        img_all.append(one_img)
        one_img = []



# 开始对每一张图片生成xml文件
for single in img_all:
    # print(single)
    data = single[0]
    # print(data)

    img_name = data['filename']  # 获取图像名字
    file_path = '/mnt/xfs_snode21/lambda-cloud/data/myh_data_96/BDD100K/images/100k'
    img_folder = os.path.join(file_path, 'val')
    img_path = os.path.join(img_folder, img_name)  #得到图像绝对路径
    # print(img_path)

    ##########################按照绝对路径打开图像并读取长宽高size
    img = io.imread(img_path)
#    io.imshow(img)
    w = img.shape[0]
    h = img.shape[1]
    d = img.shape[2]

    ##################get the coordinates of the bbox, name, truncated, occluded（object的子节点们，需要循环）
    for element in single:
        if 'box2d' in element:
            x1.append(element['box2d']['x1'])
            x2.append(element['box2d']['x2'])
            y1.append(element['box2d']['y1'])
            y2.append(element['box2d']['y2'])
            classname.append(element['name'])
            if element['truncated']==True:
                truncate.append('1')
            else:
                truncate.append('0')
            if element['occluded']==True:
                occlude.append('1')
            else:
                occlude.append('0')


    # print(truncate)
    # print(occlude)

    annotation = ET.Element("annotation")
    #创建annotation的子节点folder，并添加数据
    folder = ET.SubElement(annotation,"folder")
    folder.text = 'BDD 100K'
    #创建annotation的子节点filename，并添加属性
    filename = ET.SubElement(annotation,"filename")
    filename.text = img_name
    #创建annotation的子节点source，并添加属性
    source = ET.SubElement(annotation,"source")
    #
    size = ET.SubElement(annotation, "size")
    #
    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = '0'


    #################object
    for i in range(0, len(x1)):
        object = ET.SubElement(annotation, "object")
        #object的六个子节点
        name = ET.SubElement(object, 'name')
        name.text = classname[i]
        #
        pose = ET.SubElement(object, 'pose')
        pose.text = "Unspecified"
        #
        truncated = ET.SubElement(object, 'truncated')
        truncated.text = truncate[i]
        #
        occluded = ET.SubElement(object, 'occluded')
        occluded.text = occlude[i]
        #
        bndbox = ET.SubElement(object, 'bndbox')

        #
        difficult = ET.SubElement(object, 'difficult')
        difficult.text = "0"
        #

        #子节点bndbox下的四个子节点
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(x1[i])
        #
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(y1[i])
        #
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(x2[i])
        #
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(y2[i])
    #####################################

    #source的三个子节点
    database = ET.SubElement(source,"database")
    database.text = "bdd_100k_database"
    #
    annotation_1 = ET.SubElement(source,"annotation")
    annotation_1.text = "bdd_100k_database"
    #
    image = ET.SubElement(source,"image")
    image.text = "flickr"
    #

    #size的三个子节点
    width = ET.SubElement(size,"width")
    width.text = str(w)
    #
    height = ET.SubElement(size,"height")
    height.text = str(h)
    #
    depth = ET.SubElement(size,"depth")
    depth.text = str(d)
    #



    prettyXml(annotation, '\t', '\n')            #执行美化方法
    tree = ET.ElementTree(annotation)

    xml_name = data['filename'] + '.xml'

    tree.write(xml_name)

    print(data['filename'], 'finished')

    x1 = []
    y1 = []
    x2 = []
    y2 = []
    classname = []
    truncate = []
    occlude = []
