import face_recognition as fr
import cv2
import numpy as np
import os

path = "./train/"

known_names = []
known_name_encodings = []

images = os.listdir(path)
for _ in images:
    image = fr.load_image_file(path + _)
    image_path = path + _
    encoding = fr.face_encodings(image)[0]

    known_name_encodings.append(encoding)
    known_names.append(os.path.splitext(os.path.basename(image_path))[0].replace("_", " ").title())

print(known_names)

# Inicijalizacija web kamere (0 označava prvu dostupnu kameru)
video_capture = cv2.VideoCapture(0)

while True:
    # Čitanje frejma s web kamere
    ret, frame = video_capture.read()

    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if face_distances[best_match] < 0.95:
            if matches[best_match]:
                name = known_names[best_match]
            else:
                name = "Nepoznato"
        else:
            name = "Nepoznato"

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.3, (255, 255, 255), 1)

    # Prikazivanje rezultata u prozoru
    cv2.imshow("Result", frame)

    # Prekid petlje pritiskom na tipku 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Oslobađanje resursa nakon završetka
video_capture.release()
cv2.destroyAllWindows()
