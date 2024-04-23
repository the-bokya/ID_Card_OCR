import cv2
import pytesseract
import re
import numpy as np


contrast = lambda x: np.divide((np.tanh(x * 4 - 1.3) + 1), 2)


def cv2_chi_jadu(d=dict(), fields=["Class", "DOB", "Mobile", "Blood group"]):
    cap = cv2.VideoCapture(0)
    i = 0
    kernel = np.ones((1, 1), np.uint8)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # blurred = cv2.GaussianBlur(frame, (5, 5), 5.0)
            # frame = np.clip((frame - 0.5 * blurred) * 1.5, 0, 255).astype("uint8")
            # frame = cv2.equalizeHist(frame)
            # frame = cv2.fastNlMeansDenoising(frame, 5, 3, 11)
            blurred = cv2.GaussianBlur(frame, (11, 11), 7.0)
            frame = np.clip((frame - 0.4 * blurred) * 1.5, 0, 255).astype("uint8")
            frame = np.clip(np.power(frame, 1.4) // (9), 0, 255).astype("uint8")
            # frame = np.clip(frame - 0.1*(frame - cv2.equalizeHist(frame)), 0, 255)
            # frame = contrast(np.divide(frame, 255)) * 255

            frame = frame.astype("uint8")
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == ord("q"):
                cv2.destroyAllWindows()
                cap.release()
                break
            if i % 10 == 0:
                # cv2.imwrite("cap.jpg", frame)
                print(d)
                txt = pytesseract.image_to_string(frame)
                # cv2.imwrite('cap.jpg', frame)
                name_line = 0
                prn_found = False
                next_dob = False
                for t in txt.split("\n"):
                    if next_dob:
                        d["DOB"] = t
                        next_dob = False
                    for field in fields:

                        if field.lower() in t.lower():
                            d[field] = re.findall(
                                f"{field.lower()}[: ]*(.*)", t.lower()
                            )[0]

                        if field == "DOB":
                            field = "date of birth"
                            if field.lower() in t.lower():
                                next_dob = True
                                d["DOB"] = re.findall(
                                    f"{field.lower()}[: ]*(.*)", t.lower()
                                )[0]
                    name = re.fullmatch("([A-Z][ ]*)+", t)
                    if not name:
                        name2 = re.findall("[A-Z][a-z]+", t)
                        if len(name2) >= 3 and ":" not in t and "Designation" not in t:
                            name2 = " ".join(name2)
                            d["Name"] = name2
                    prn = re.findall("202" + "[0-9]" * 9, t)
                    if len(prn) == 1:
                        d["PRN"] = prn[0]
                    if name_line == 0:
                        if not name:
                            continue
                        if len(name[0].split(" ")) == 2:
                            prev_name = name
                            name_line = 1
                        if len(name[0].split(" ")) == 3:
                            d["Name"] = name[0]
                    if name_line == 1:
                        if name:
                            d["Name"] = prev_name[0] + name[0]
                        else:
                            name_line = 0

            i += 1


if __name__ == "__main__":
    cv2_chi_jadu()
