import cv2

cap = cv2.VideoCapture(0)
i = 0
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("frame", frame)
        if cv2.waitKey(10) == ord("q"):
            cv2.imwrite("cap.jpg", frame)
            cv2.destroyAllWindows()
            cap.release()
            break
