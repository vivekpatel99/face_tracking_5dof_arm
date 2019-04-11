# Created by viv at 27.03.19

import cv2
import time
from imutils.video import VideoStream
from imutils.video import FPS

END_TIME = 30

# ------------------------------------------------------------------------------
# """ cam run  """
# ------------------------------------------------------------------------------
def camera_run():
    t_end = time.time() + END_TIME
    fps = FPS().start()

    cap = cv2.VideoCapture(0)

    while time.time() < t_end:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        fps.update()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        print('Camera is not Connected')

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    # stop the timer and display FPS information
    fps.stop()
    print("Elapsed time: {:.2f}".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))


# ------------------------------------------------------------------------------
# """ cam run  """
# ------------------------------------------------------------------------------
def camera_run_opt():
    t_end = time.time() + END_TIME

    fps = FPS().start()

    cap = VideoStream(0).start()

    while time.time() < t_end:

        # Capture frame-by-frame
        frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)
        fps.update()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        print('Camera is not Connected')

    fps.stop()
    # When everything done, release the capture
    cv2.destroyAllWindows()
    cap.stop()

    # stop the timer and display FPS information

    print("Elapsed time: {:.2f}".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))


if __name__ == '__main__':
    camera_run()
    camera_run_opt()
