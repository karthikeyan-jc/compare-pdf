from flask import send_file, jsonify
from werkzeug.utils import secure_filename
import os
from pdf2image import convert_from_path
import cv2
import imutils
from skimage.metrics import structural_similarity as compare_ssim
import time
from PIL import Image

upload_folder='./uploads'
approved_extension='.pdf'

def is_compatible(file1,file2):
    approved_filetype=False
    filename1, file_extension1 = os.path.splitext(file1.filename)
    filename2, file_extension2 = os.path.splitext(file2.filename)
    return (file_extension1==file_extension2 and file_extension1==approved_extension)
    

def compare(file1, file2):
    if not is_compatible(file1,file2):
        return jsonify({"error":"Incompatible files. Please upload two PDF files."}),403
    ts = time.time()
    filename = secure_filename(str(ts)+"_file1.pdf")
    file1.save(os.path.join(upload_folder, filename))
    filename = secure_filename(str(ts)+"_file2.pdf")
    file2.save(os.path.join(upload_folder,filename))
    
    pages1 = convert_from_path(upload_folder+"/"+str(ts)+"_file1.pdf")
    size1=len(pages1)
    pages2 = convert_from_path(upload_folder+"/"+str(ts)+"_file2.pdf")
    size2=len(pages2)

    if(size1 != size2):
        return jsonify({"error":"Number of pages in both PDF files doesn't match. Not eligible for comparison"}),403

    for i in range(0, size1):
        pages1[i].save(str(ts)+"_file1_"+str(i//1)+".jpg",'JPEG')

    for i in range(0, size2):
        pages2[i].save(str(ts)+"_file2_"+str(i//1)+".jpg",'JPEG')
        
    imagesFile1=[]
    for i in range(0,size1):
        imagesFile1.append(cv2.imread(str(ts)+"_file1_"+str(i//1)+".jpg"))
    
    imagesFile2=[]
    for i in range(0, size2):
        imagesFile2.append(cv2.imread(str(ts)+"_file2_"+str(i//1)+".jpg"))
    
    for i in range(0, size1):
        imageA=imagesFile1[i]
        imageB=imagesFile2[i]
        
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        height, width, channels = imageA.shape
        imageA = cv2.resize(imageA, (width//2, height//2)) 
        height, width, channels = imageB.shape
        imageB = cv2.resize(imageB, (width//2, height//2)) 
        im_h = cv2.hconcat([imageA, imageB])
        cv2.imwrite(str(ts)+"_change_"+str(i//1)+".jpg", im_h)
    changeImages=[]
    image1=Image.open(str(ts)+"_change_0"+".jpg")
    for i in range(1, size1):
        changeImages.append(Image.open(str(ts)+"_change_"+str(i//1)+".jpg"))
    image1.save(str(ts)+"_final.pdf","PDF",resolution=100.0,save_all=True,append_images=changeImages)
    for i in range(0,size1):
        os.remove(str(ts)+"_file1_"+str(i//1)+".jpg")
        os.remove(str(ts)+"_file2_"+str(i//1)+".jpg")
        os.remove(str(ts)+"_change_"+str(i//1)+".jpg")
    os.remove(upload_folder+"/"+str(ts)+"_file1.pdf")
    os.remove(upload_folder+"/"+str(ts)+"_file2.pdf")
    response= send_file("./"+str(ts)+"_final.pdf", mimetype='application/pdf',attachment_filename='output.pdf',as_attachment=True)
    os.remove("./"+str(ts)+"_final.pdf")
    return response