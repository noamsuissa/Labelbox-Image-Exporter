
import json
import os
import requests

dataset_name = "Popliteal_dataset"
test_dir = "test"
images_dir = "images"
masks_dir = "masks"
export_path = "C:\\Users\\Noam Suissa\\Downloads"

def download_image(pic_url, path):
    with open(path, 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response, path)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

#create dirs
path = os.path.join(export_path, dataset_name)

path2 = os.path.join(path, test_dir)

path3 = os.path.join(path2, images_dir)

path4 = os.path.join(path2, masks_dir)

if not os.path.exists(path):
	os.mkdir(path)
	os.mkdir(path2)
	os.mkdir(path3)
	os.mkdir(path4)

#open labelbox json
fp = open("C:\\Users\\Noam Suissa\\Downloads\\Popliteal_test_consensus.json")

jsn = json.load(fp)

#populate dirs
for i in jsn:
	
	id_ = i["DataRow ID"]
	original_img_url = i["Labeled Data"]
	objects = i["Label"]["objects"]

	#download original image
	download_path = path3 + '/' +id_ + '.png'
	if not os.path.exists(download_path):
		download_image(original_img_url, download_path)

	im_path = os.path.join(path4, id_)
	if not os.path.exists(im_path):
		os.mkdir(im_path)

	labeler = i["Created By"].split('@')[0]

	if labeler == "kes401":
		labeler = "Dr.Moghrabi"
	if labeler == "ningnanw":
		labeler = "Dr.Wang"
	if labeler == "pascal.laferriere-langlois":
		labeler = "Dr.Godbout-Simard"
	if labeler == "pllanglois":
		labeler = "Dr.Laferriere-Langlois"

	labeler_path = os.path.join(im_path, labeler)
	if not os.path.exists(labeler_path):
			os.mkdir(labeler_path)

	#download masks
	for o in objects:
		name = o["value"]
		link = o["instanceURI"]
		ob_path = os.path.join(labeler_path, name)
		
		if not os.path.exists(ob_path):
			os.mkdir(ob_path)
		
		obj_download_path = ob_path + '/' +id_ + '.png'
		if not os.path.exists(obj_download_path):
			download_image(link, obj_download_path)

