import cv2
import numpy as np

# Game window dimensions
width, height = 640, 480

# Ball properties
ball_pos = [320, 240]
ball_radius = 15
ball_speed = [4, 4]

# Paddle properties
paddle_width = 100
paddle_height = 15
paddle_y = height - 30
paddle_x = 270  # initial

# Score
score = 0

# Open webcam
cap = cv2.VideoCapture(0)

def detect_color(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the biggest contour
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx = x + w // 2
        return cx
    return None

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # mirror effect
    frame = cv2.resize(frame, (width, height))

    # Detect red object
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    cx = detect_color(frame, lower_red, upper_red)

    if cx:
        paddle_x = max(0, min(cx - paddle_width // 2, width - paddle_width))

    # Move ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Wall collision
    if ball_pos[0] <= ball_radius or ball_pos[0] >= width - ball_radius:
        ball_speed[0] *= -1
    if ball_pos[1] <= ball_radius:
        ball_speed[1] *= -1

    # Paddle collision
    if (paddle_y < ball_pos[1] + ball_radius < paddle_y + paddle_height and
        paddle_x < ball_pos[0] < paddle_x + paddle_width):
        ball_speed[1] *= -1
        score += 1  # increase score on paddle hit

    # Bottom collision - Game Over
    if ball_pos[1] >= height - ball_radius:
        cv2.putText(frame, "Game Over", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        cv2.putText(frame, f"Score: {score}", (230, 260), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        cv2.imshow("Game", frame)
        cv2.waitKey(3000)
        break

    # Draw ball and paddle
    cv2.circle(frame, tuple(ball_pos), ball_radius, (255, 0, 0), -1)
    cv2.rectangle(frame, (paddle_x, paddle_y), (paddle_x + paddle_width, paddle_y + paddle_height), (0, 255, 0), -1)

    # Draw score
    cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Game", frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
