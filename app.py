import io
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from flask import Flask, redirect,jsonify, url_for, request
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import utils




app = Flask(__name__)

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'static/uploads/images'), exist_ok=True)



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        # model = utils.intializePredectionModel()

        image = request.files['file']
        # image.save(os.path.join(app.instance_path, 'static/uploads/images', secure_filename(image.filename)))
        filestr = request.files['file'].read()
        #convert string data to numpy array
        npimg = np.fromstring(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        heightImg = 450
        widthImg = 450
        img = cv2.resize(img, (widthImg, heightImg))
        cv2.imwrite("filename1.png", img)
        imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
        cv2.imwrite("filename2.png", imgBlank)

        #### 1. PREPARE THE IMAGE
        imgThreshold = utils.preProcess(img)
        cv2.imwrite("filename3.png", imgThreshold)


        # #### 2. FIND ALL COUNTOURS
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS
     

        #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
        biggest, maxArea = utils.biggestContour(contours) # FIND THE BIGGEST CONTOUR
        print(biggest)
        if biggest.size != 0:
             biggest = utils.reorder(biggest)
             print(biggest)
             cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
             pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
             pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
             matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
             imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
             imgDetectedDigits = imgBlank.copy()
             imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
             cv2.imwrite("filename4.png", imgWarpColored)

             #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
            #  imgSolvedDigits = imgBlank.copy()
            #  boxes = utils.splitBoxes(imgWarpColored)
            #  print(len(boxes))
            #  # cv2.imshow("Sample",boxes[65])
            #  numbers = utils.getPredection(boxes, model)
            #  print(numbers)
            #  imgDetectedDigits = utils.displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
            #  numbers = np.asarray(numbers)
            #  posArray = np.where(numbers > 0, 0, 1)
            #  print(posArray)

        
        

        return jsonify({"status":200, "message" : "Sudoku Solved" })
    else:
        return "Pfggg"
    

if __name__ == "__main__":
    app.run(debug=True)