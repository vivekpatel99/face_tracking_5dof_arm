# Created by viv at 16.03.19
import cv2
import numpy as np

TASK_TITLE = 'TASK: Feature Detection is running...'
TASK_INFO = 'TASK INFO: Please move the zybo box'


# ------------------------------------------------------------------------------
# """ face_recog_pygm """
# ------------------------------------------------------------------------------
class FeatureDetection:
    def __init__(self, min_match_count=30, image_path=r'tasks/feat_detect/zybo_box.png'):
        self.min_match_count = min_match_count
        self.detector = cv2.xfeatures2d.SIFT_create()
        flann_index_kditree = 0
        self.flann_param = dict(algorithm=flann_index_kditree, tree=5)
        self.flann = cv2.FlannBasedMatcher(self.flann_param, {})

        image = cv2.imread(image_path, 0)
        self.trainImg = cv2.resize(image, (640, 460))
        self.trainKP, self.trainDesc = self.detector.detectAndCompute(self.trainImg, None)

    def run_feat_detect(self, QueryImgBGR):
        QueryImg = cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2GRAY)
        queryKP, queryDesc = self.detector.detectAndCompute(QueryImg, None)
        matches = self.flann.knnMatch(queryDesc, self.trainDesc, k=2)

        goodMatch = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)

        if len(goodMatch) > self.min_match_count:
            tp = []
            qp = []
            for m in goodMatch:
                tp.append(self.trainKP[m.trainIdx].pt)
                qp.append(queryKP[m.queryIdx].pt)
            tp, qp = np.float32((tp, qp))
            H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)
            h, w = self.trainImg.shape

            trainBorder = np.float32([[[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]])
            query_border = cv2.perspectiveTransform(trainBorder, H)
            query_border = np.int32(query_border)
            cv2.polylines(QueryImgBGR, [query_border], True, (0, 255, 0), 2)
            query_border = query_border.flatten()
            half_height_y = int((query_border[1] + query_border[3]) / 2)
            half_width_x = int(((query_border[2] + query_border[4]) / 2))

            cv2.circle(QueryImgBGR, (half_width_x, half_height_y), 2, (0, 0, 255), 8)
            # cv2.circle(QueryImgBGR, (200, 200), 3, (0, 0, 255), 10)

            return QueryImgBGR
        # else:
        # print("Not Enough match found- %d/%d" % (len(goodMatch), self.min_match_count))


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
        ret, QueryImgBGR = cam.read()
        QueryImg = cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2GRAY)
        queryKP, queryDesc = detector.detectAndCompute(QueryImg, None)
        matches = flann.knnMatch(queryDesc, trainDesc, k=2)

        goodMatch = []
        for m, n in matches:
            if (m.distance < 0.75 * n.distance):
                goodMatch.append(m)
        if (len(goodMatch) > MIN_MATCH_COUNT):
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
            cv2.polylines(QueryImgBGR, [np.int32(queryBorder)], True, (0, 255, 0), 5)
        else:
            print("Not Enough match found- %d/%d" % (len(goodMatch), MIN_MATCH_COUNT))
        cv2.imshow('result', QueryImgBGR)
        if cv2.waitKey(10) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
