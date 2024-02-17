import os
from datetime import datetime
from ultralytics import YOLO
import cv2
import string
from paddleocr import PaddleOCR
from firebase import firebase
from PIL import Image, ImageDraw, ImageFont
import qrcode


qr = qrcode.QRCode(
    version=3,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=6,
    border=1,
)

FBconn = firebase.FirebaseApplication("https://parcare-7f4bc-default-rtdb.europe-west1.firebasedatabase.app/")

lista=[]
variabile=""

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'Q': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

def extract_letters_and_numbers(input_string):
    return ''.join(char for char in input_string if char.isalnum())


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """
    modified_text = []

    if text[0] == 'B' \
            and text[1] in string.digits \
            and text[2] in string.digits \
            and text[3] in string.ascii_uppercase \
            and text[4] in string.ascii_uppercase \
            and text[5] in string.ascii_uppercase:

        if text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys():
            modified_text.append(text[0])
            modified_text.append('_')
        if text[1] in string.digits or text[1] in dict_char_to_int.keys():
            modified_text.append(text[1])
        if text[2] in string.digits or text[2] in dict_char_to_int.keys():
            modified_text.append(text[2])
            modified_text.append('_')
        if text[3] in string.ascii_uppercase or text[3] in dict_char_to_int.keys():
            modified_text.append(text[3])
        if text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys():
            modified_text.append(text[4])
        if text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys():
            modified_text.append(text[5])

    elif text[0] == 'B' \
            and text[1] in string.digits\
            and text[2] in string.digits \
            and text[3] in string.digits\
            and text[4] in string.ascii_uppercase \
            and text[5] in string.ascii_uppercase \
            and text[6] in string.ascii_uppercase:

        if text[0] in string.ascii_uppercase:
            modified_text.append(text[0])
            modified_text.append('_')
        if text[1] in string.digits :
            modified_text.append(text[1])
        if text[2] in string.digits:
            modified_text.append(text[2])
        if text[3] in string.digits:
            modified_text.append(text[3])
            modified_text.append('_')
        if text[4] in string.ascii_uppercase:
            modified_text.append(text[4])
        if text[5] in string.ascii_uppercase:
            modified_text.append(text[5])
        if text[6] in string.ascii_uppercase:
            modified_text.append(text[6])

    elif text[0] in string.ascii_uppercase \
            and text[1] in string.ascii_uppercase \
            and text[2] in string.digits \
            and text[3] in string.digits \
            and text[4] in string.ascii_uppercase \
            and text[5] in string.ascii_uppercase \
            and text[6] in string.ascii_uppercase:
        if text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys():
            modified_text.append(text[0])
        if text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys():
            modified_text.append(text[1])
            modified_text.append('_')
        if text[2] in string.digits or text[2] in dict_char_to_int.keys():
            modified_text.append(text[2])
        if text[3] in string.digits or text[3] in dict_char_to_int.keys():
            modified_text.append(text[3])
            modified_text.append('_')
        if text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys():
            modified_text.append(text[4])
        if text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys():
            modified_text.append(text[5])
        if text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys():
            modified_text.append(text[6])
    else:
        return text

    final_text = ''.join(modified_text)

    return final_text


PHOTO_DIR = os.path.join('.', 'photos')
number_palate = ""

# Read webcam
webcam = cv2.VideoCapture(0) 

model_path = os.path.join('models/license_plate_detector.pt')

license_plate_detector = YOLO(model_path)  # load a custom model

threshold = 0.5

while True: 
    ret, frame = webcam.read()
    # Display the frame
    cv2.imshow('Frame', frame)

    key = cv2.waitKey(40) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):

        # Capture screenshot and save with current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M")

        screenshot_path = os.path.join(PHOTO_DIR, f'screenshot_{timestamp}.png')
        print(timestamp)
        cv2.imwrite(screenshot_path, frame)
        image = cv2.imread(screenshot_path)

        try:

            license_plates = license_plate_detector(image)[0]
            for license_plate in license_plates.boxes.xyxy:
                x1 , y1, x2, y2 = license_plate

            # crop the license plate

            new_x1 = int(x1 + ((x2-x1)*0.085))
            new_x2 = int(x2 - ((x2-x1)*0.05))
            new_y1 = int(y1 + ((y2-y1)*0.04))
            new_y2 = int(y2 - ((y2-y1)*0.04))

            license_plate_crop = image[new_y1:new_y2, new_x1:new_x2,:]

            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

            bfilter = cv2.bilateralFilter(license_plate_crop_gray, 11, 17, 17)  # Noise reduction
        
            license_plate_crop_treshold = cv2.adaptiveThreshold(bfilter, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 41, 4)
            cv2.imshow('license_plate_crop_treshold', license_plate_crop_treshold)

            ocr = PaddleOCR(use_angle_cls=True, lang='en')
            result = ocr.ocr(license_plate_crop_treshold, det=True, cls=True)
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    print(line)

            #print the ticket
            print("____BUNA ZIUA____")
            print(f"{timestamp[0:4]}/{timestamp[4:6]}/{timestamp[6:8]}")
            print("ORA INTRARE:")
            print(f"{timestamp[9:11]}:{timestamp[11:13]}")
            print("ORA DE IESIRE:")
            print(f"{int(timestamp[9:11]) + 1}:{timestamp[11:13]}")
            print("NUMBER PLATE:")
        
            variabile=""
            lista=[]

            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    lista.append(line[1])

            max = lista[0][-1]
            # print(type(max))
            for element in lista:
                if element[-1] >= max:
                    max = element[-1]
                    # print(element[0])
                    variabile=str(license_complies_format(element[0].replace(" ", "").upper()))
                    variabila=str(extract_letters_and_numbers(variabile))

            print(variabila)

            data_to_upload= {
                'numar_inmatriculare' : variabila,
                'ora_intrare' : str(timestamp[9:11])+ ":" + str(timestamp[11:13]),
                'ora_iesire' : str((int(timestamp[9:11])+1)) + ":" + str(timestamp[11:13]),
                'data' : str((int(timestamp[6:8]))) + "." + str(timestamp[4:6])+ "." + str(timestamp[0:3])
            }
            
            resultat = FBconn.post("/MyTestData", data_to_upload)
            print(resultat)
            print("____LA REVEDERE____")

            nume_ticket = variabila + "_" + str((int(timestamp[6:8]))) + str(timestamp[4:6])+ str(timestamp[0:4])+"_" + str(timestamp[9:11])+ str(timestamp[11:13])+"_"+str((int(timestamp[9:11])+1)) + str(timestamp[11:13])

            data = nume_ticket
            qr.add_data(data)
            qr.make(fit=True)

            # Create an image from the QR Code instance
            img_qr = qr.make_image(fill_color="black", back_color="white")
            # Create a blank image
            image = Image.new("RGB", (250, 400), "white")
            draw = ImageDraw.Draw(image)

            # Add text and details to the image
            font_size=22
            font = ImageFont.load_default()
            font1 = ImageFont.truetype("C:/Users/PC/Desktop/proiectse2/fonts/Arial.ttf",font_size)
            font2 = ImageFont.truetype("C:/Users/PC/Desktop/proiectse2/fonts/Arial.ttf",font_size-7)
            draw.text((57, 30), "Parking Ticket", fill="black", font=font1)
            draw.text((15, 75), "Numar inmatriculare: "+str(variabila), fill="black", font=font2)
            draw.text((15, 100), "Data: "+str((int(timestamp[6:8]))) + "." + str(timestamp[4:6])+ "." + str(timestamp[0:4]), fill="black", font=font2)
            draw.text((15, 125), "Ora de intrare: "+str(timestamp[9:11])+ ":" + str(timestamp[11:13]), fill="black", font=font2)
            draw.text((15, 150), "Ora de iesire: "+str((int(timestamp[9:11])+1)) + ":" + str(timestamp[11:13]), fill="black", font=font2)
            
            image.paste(img_qr,(31,185))
            # Save the image to a folder
            image.save("C:/Users/PC/Desktop/proiectse2/ticket/"+nume_ticket+".png")
            data=""
            print("Parking ticket image created and saved.")

        except Exception as e:
            print("something gone wrong:((((")
            print(e)


    #delete the screen from folder
if os.path.exists(screenshot_path):
    os.remove(screenshot_path)

webcam.release()
cv2.destroyAllWindows()

