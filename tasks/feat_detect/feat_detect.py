# Created by viv at 16.03.19
import cv2
import numpy as np

TASK_TITLE = 'TASK: Feature Detection is running...'
TASK_INFO = 'TASK INFO: Please move the zybo box'


# ------------------------------------------------------------------------------
# """ face_recog_pygm """
# ------------------------------------------------------------------------------
class FeatureDetection:
    """ Feature Detection class """

    def __init__(self, min_match_count=30, image_path=r'tasks/feat_detect/zybo_box.png'):
        self.min_match_count = min_match_count

        # Scale Invariant Feature Transform (SIFT)
        self.detector = cv2.xfeatures2d.SIFT_create()  # SIFT extraction
        flann_index_kditree = 0  # Initialize the flag (it is not in built in openCV)
        self.flann_param = dict(algorithm=flann_index_kditree, tree=5)
        self.flann = cv2.FlannBasedMatcher(self.flann_param, {})  # openCV bug, therefore empty dict is given

        image = cv2.imread(image_path, 0)
        self.train_img = cv2.resize(image, (640, 460))
        self.trainKP, self.trainDesc = self.detector.detectAndCompute(self.train_img, None)

    # -------------------------------------------------------------------
    # """ run_feat_detect """
    # -------------------------------------------------------------------
    def run_feat_detect(self, query_img_bgr, frame_display_indx):
        query_img = cv2.cvtColor(query_img_bgr, cv2.COLOR_BGR2GRAY)
        query_kp, query_desc = self.detector.detectAndCompute(query_img, None)
        matches = self.flann.knnMatch(query_desc, self.trainDesc, k=2)

        good_match = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_match.append(m)

        if len(good_match) > self.min_match_count:
            tp = []
            qp = []
            for m in good_match:
                tp.append(self.trainKP[m.trainIdx].pt)
                qp.append(query_kp[m.queryIdx].pt)
            tp, qp = np.float32((tp, qp))
            H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)
            h, w = self.train_img.shape

            train_border = np.float32([[[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]])
            query_border = cv2.perspectiveTransform(train_border, H)
            query_border = np.int32(query_border)
            cv2.polylines(query_img_bgr, [query_border], True, (0, 255, 0), 2)
            query_border = query_border.flatten()

            half_height_y = int((query_border[1] + query_border[3]) / 2)
            half_width_x = int((query_border[2] + query_border[4]) / 2)

            cv2.circle(query_img_bgr, (half_width_x, half_height_y), 2, (0, 0, 255), 8)
            if frame_display_indx == 0:
                out_frame = cv2.cvtColor(query_img_bgr, cv2.COLOR_BGR2RGB)
            elif frame_display_indx == 1:
                out_frame = query_img_bgr
            else:
                out_frame = query_img_bgr
            return (half_width_x, half_height_y), out_frame


def main():
    MIN_MATCH_COUNT = 30

    detector = cv2.xfeatures2d.SIFT_create()

    FLANN_INDEX_KDITREE = 0
    flannParam = dict(algorithm=FLANN_INDEX_KDITREE, tree=5)
    flann = cv2.FlannBasedMatcher(flannParam, {})

    trainImg = cv2.imread(r'zybo_boxzybo_box.png', 0)
    trainImg = cv2.resize(trainImg, (640, 460))
    # trainKP,trainDesc=detector.detectAndCompute(trainImg,None)
    trainKP, trainDesc = detector.detectAndCompute(trainImg, None)

    cam = cv2.VideoCapture(0)
    while True:
        ret, query_img_bgr = cam.read()
        QueryImg = cv2.cvtColor(query_img_bgr, cv2.COLOR_BGR2GRAY)
        queryKP, queryDesc = detector.detectAndCompute(QueryImg, None)
        matches = flann.knnMatch(queryDesc, trainDesc, k=2)

        goodMatch = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)
        if len(goodMatch) > MIN_MATCH_COUNT:
            tp = []
            qp = []
            for m in goodMatch:
                tp.append(trainKP[m.trainIdx].pt)
                qp.append(queryKP[m.queryIdx].pt)
            tp, qp = np.float32((tp, qp))
            H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)
            h, w = trainImg.shape
            trainBorder = np.float32([[[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]])
            queryBorder = cv2.perspectiveTransform(trainBorder, H)
            cv2.polylines(query_img_bgr, [np.int32(queryBorder)], True, (0, 255, 0), 5)
        else:
            print("Not Enough match found- %d/%d" % (len(goodMatch), MIN_MATCH_COUNT))
        cv2.imshow('result', query_img_bgr)
        if cv2.waitKey(10) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
