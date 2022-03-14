from constant import *
import cv2
import json

# NetworkTables
# Find Avg Circles

# Implement Later
angle = 0.0
ballExists = False
teamBallAligned = False
# isEnemyBallAlligned = False

path = "./data/moving.mp4"
cam = cv2.VideoCapture(path)

while (True):
    ret, frame = cam.read()
    # # For Video Version (Temp)
    frame = cv2.resize(frame, (324, 576), interpolation = cv2.INTER_LINEAR)
    # ###################

    width, height = frame.shape[1], frame.shape[0]

    mask = None
    if (TEAM == Color.Red):
        convert = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(convert, LIGHT_RED, DARK_RED)
    else:
        convert = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(convert, LIGHT_BLUE, DARK_BLUE)

    output = cv2.bitwise_and(frame, frame, mask=mask)
    gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
    gray_blurred = cv2.blur(gray, (7, 7))

    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=40, param2=30, minRadius=40,  maxRadius=200)

    if circles is not None:
        ballExists = True
        angle = circles[0][0][0] - int(width / 2)
        middle = abs(angle) <= INTAKE_OFFSET
        if (middle):
            teamBallAligned = True
        else:
            teamBallAligned = False
        # Temp for User Visuals #
        circles = np.uint16(np.around(circles))
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 3)
        # End of Visuals #
    else:
        angle = 0.0
        ballExists = False

    # Draw Dev (Temp)
    cv2.line(frame, (int(width / 2), 0), (int(width / 2), height), (0, 90, 255), 3)
    cv2.rectangle(frame, (0, 0), (130, 80), (255, 255, 255), -1)
    cv2.putText(frame, str(teamBallAligned), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 90, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, str(round(angle / (width / 2), 3)), (5, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 90, 255), 2, cv2.LINE_AA)
    cat = cv2.hconcat([frame, output])
    cv2.imshow(f"Color Mask : Team - {TEAM.value}", cat)

    data = {
        "protocol": PROTOCOL,
        "fov": FOV,
        "angle": angle,
        "ballExists": ballExists,
        "ballAligned": teamBallAligned,
        "ballTeam": TEAM.value
    }

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cam.release()
