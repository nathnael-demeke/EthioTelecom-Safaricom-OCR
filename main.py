import cv2
import pytesseract
import re 

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
print("service started...")
while True:
    try:
        number = input("please enter image number: ")
        cropped_image = cv2.imread(f"dataset\\{number}(cropped).jpg")
        full_image = cv2.imread(f"dataset\\{number}.jpg")




        def get_text_from_image(cropped_image,full_image):
            full_text = pytesseract.image_to_string(full_image)
            card_text = pytesseract.image_to_string(cropped_image)

            return {"CardText": card_text, "FullText":full_text}

        def what_Organization(All_text):
            full_text = All_text["FullText"]
            card_text = All_text["CardText"]
            organization_pin = {
                "EthioTelecom": ["805", "*805*", "*805#","*805*Pin#", "Retailer","retailer","Telecom"],
                "SafariCom": ["705", "*705*", "*705#","Agent","agent", "Agent:"]
            }
            identified_as = "N/A"
            for organization_name in organization_pin.keys():
                patterns = organization_pin[organization_name]
                for pattern in patterns: 
                    try:
                        text_splited = full_text.split()
                        for word in text_splited:
                            if pattern == word:
                                identified_as = organization_name
                                break
                    except:
                        return (str(pattern) + " checked...")
            return identified_as

        def arrange_card_text(card_text):
            card_text = re.findall(pattern=r"[0-9]",string=card_text)
            card_text = ''.join(card_text)
            return card_text
        All_text = get_text_from_image(cropped_image=cropped_image, full_image=full_image)
        card_text = arrange_card_text(All_text["CardText"])
        full_image_information = {"CardText": card_text, "Organization": what_Organization(All_text)}
        print(f"[Image] {number}.jpg ")
        print("[CARD INFORMATION] " + str(full_image_information))
    except Exception as error:
        print(error)