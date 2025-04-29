import cv2
import numpy as np

# Inicializar el filtro de Kalman
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

# Captura de video
cap = cv2.VideoCapture('canva.mp4')

# Obtener las dimensiones originales del video
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Definir las nuevas dimensiones del video para mostrarlo más pequeño
new_width = original_width // 2
new_height = original_height // 2

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar el frame para mostrarlo más pequeño
    frame_resized = cv2.resize(frame, (new_width, new_height))

   #Definir a espacio de color HSV
    hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)

    # Definir el rango de color blanco en HSV
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])

    # Crear una máscara para el color blanco
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Aplicar operaciones morfológicas
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 510:  # Ajusta este valor según el tamaño de la pelota
            # Filtrar por forma circular
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 0.7 < circularity < 1.2:  # Ajusta estos valores según sea necesario
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(frame_resized, center, radius, (0, 255, 0), 2)

                # Actualizar el filtro de Kalman
                measurement = np.array([[np.float32(center[0])], [np.float32(center[1])]])
                kalman.correct(measurement)
                prediction = kalman.predict()
                predict_pt = (int(prediction[0]), int(prediction[1]))

                # Dibujar la predicción
                cv2.circle(frame_resized, predict_pt, radius, (0, 0, 255), 2)

                # Agregar etiqueta
                cv2.putText(frame_resized, 'Pelota', (center[0] - radius, center[1] - radius - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Mostrar el frame redimensionado
    cv2.imshow('Frame', frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
