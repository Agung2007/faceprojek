import cv2
import mediapipe as mp
from gtts import gTTS
import playsound
import os

# ====== Inisialisasi Mediapipe ======
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Fungsi cari kamera yang aktif
def find_camera():
    for index in range(6):  # cek index 0-5
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"✅ Kamera ditemukan di index {index}")
            return cap
        cap.release()
    print("❌ Tidak ada kamera yang bisa dibuka")
    return None

# Fungsi membuat & memainkan suara
def speak(text):
    file = "voice.mp3"
    tts = gTTS(text=text, lang="id")
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)

# ====== Mulai kamera ======
cap = find_camera()
if cap is None:
    exit()

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:
    last_count = None  # supaya tidak mengulang suara terus

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Tidak bisa membaca frame dari kamera")
            break

        # Balik gambar biar seperti cermin
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        finger_count = 0

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark

                # Thumb (jempol)
                if landmarks[4].x < landmarks[3].x:
                    finger_count += 1
                # 4 jari lain
                if landmarks[8].y < landmarks[6].y:  # telunjuk
                    finger_count += 1
                if landmarks[12].y < landmarks[10].y: # tengah
                    finger_count += 1
                if landmarks[16].y < landmarks[14].y: # manis
                    finger_count += 1
                if landmarks[20].y < landmarks[18].y: # kelingking
                    finger_count += 1

        # Tampilkan teks jumlah jari
        cv2.putText(frame, f"Jari: {finger_count}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)

        # Jalankan suara hanya jika ada perubahan jumlah jari
        if finger_count != last_count:
            if finger_count == 1:
                speak("Haloo")
            elif finger_count == 2:
                speak("Perkenalkan")
            elif finger_count == 3:
                speak("Nama saya")
            elif finger_count == 4:
                speak("Agung Setiawan")
            elif finger_count == 5:
                speak("Salam kenal")
            last_count = finger_count

        cv2.imshow("Finger Voice Control", frame)

        # Tekan Q untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
