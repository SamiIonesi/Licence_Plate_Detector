# Licence_Plate_Detector
<p align="center">
  <img src="https://github.com/SamiIonesi/Licence_Plate_Detector/assets/150432462/462cc85d-9845-4b91-9f11-046a7ac75d2b" width="800" height="250">
</p>

This project has the functionality to detect the number plate of cars at the entrance of a parking lot with a camera that is placed on the entrance barrier and then when the customer presses the button it gives them a ticket with some details.

## How does it work?
Click to this [link](https://www.youtube.com/watch?v=0ZijRC7i8lM&t=1s) to see how it's working.
<p align="center">
  <img src="https://github.com/SamiIonesi/Licence_Plate_Detector/assets/150432462/392aded1-26f4-4929-86a5-95689b3703b9">
</p>
<p align = "center">
  Project Flowchart
</p>

Technologies used:
- Python – the programming language used
  - CV2 – used for image processing
  - PaddleOCR – used for converting text from images
  - YOLO – used to load the trained model for license plate detection
  - PIL – used to generate the ticket
  - Qrcode – used to generate the QR on the ticket
- Firebase - the database used
- Machine Learning – model creation

## Instructions
#### How does the code work?
The camera is used to take a picture of the car. Then with the help of YOLO and the registration number detection model, the license plate coordinates will be saved. After that we use those coordinates to apply a crop to the picture so that we can continue to read only the text that interests us, namely the registration number, with the help of PaddleOCR.
To be able to read the text properly with PaddleOCR, we apply filters and corrections to the image.
In order for the reading of the text to be as good as possible, the text must be black and not blur. We use an adaptive threshold to remove reflections from the image.
After retrieving the data from the final image, the data will be saved in the database, a prototype of the ticket will be made in the console and the actual ticket will be created.

You can see the full documentation on this [link](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FSamiIonesi%2FLicence_Plate_Detector%2Fmain%2FLicence_Plate_Detector_Documentation.docx&wdOrigin=BROWSELINK).

#### There is a few details you have to pay attention on the main code that the project to work:
1. You have to make sure that your connection to the Firebase is set correctly
   ```python
   FBconn = firebase.FirebaseApplication("put you're url to the Firebase here")
   ```
2. You have to make sure that your path to the model is set correctly
   ```python
   model_path = os.path.join('path to the licence plate detctor model')
   ```
3. You have to make sure that your path to the font is set correctly
   ```python
   font1 = ImageFont.truetype("path to the font that is in fonts folder",font_size)
   ```
4. You have to make sure that you save the ticket photo in the correct folder
   ```python
   image.save("path to the ticket folder"+nume_ticket+".png")
   ```

## Installing
#### There are several installations of libraries and connections that must be made for this project to work.
1. To install Ultralytics clik [here](https://docs.ultralytics.com/quickstart/).
2. To install CV2 click [here](https://pypi.org/project/opencv-python/#installation-and-usage).
3. To install paddleocr click [here](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/quickstart_en.md).
4. To install qrcode click [here](https://pypi.org/project/qrcode/).
5. To create a Firebase database click [here](https://www.youtube.com/watch?v=qKxisFLQRpQ&t=312s).
6. To install Firebase on Python click [here](https://pypi.org/project/firebase/) and to make connection to your Firebase database click [here](https://www.youtube.com/watch?v=mNMv3WNgp0c).
