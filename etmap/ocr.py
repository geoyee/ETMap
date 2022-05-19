from typing import List
import cv2
import numpy as np
from paddleocr.tools.infer.utility import init_args
from paddleocr.tools.infer.predict_det import TextDetector
from paddleocr.tools.infer.predict_rec import TextRecognizer


class Detector(object):
    def __init__(self) -> None:
        args = init_args().parse_args()
        args.det_model_dir = "weights/ch_PP-OCRv3_det_slim_infer"
        self.text_detector = TextDetector(args)

    def predict(self, image: np.ndarray) -> List:
        # img_size = (640, 640, 3)
        dt_boxes, _ = self.text_detector(image)
        return dt_boxes


class Recognizer(object):
    def __init__(self) -> None:
        args = init_args().parse_args()
        args.rec_model_dir = "weights/ch_PP-OCRv3_rec_slim_infer"
        args.rec_char_dict_path = "weights/ppocr_keys_v1.txt"
        self.text_recognizer = TextRecognizer(args)

    def predict(self, image_list: List) -> List:
        # img_size = (32, 320, 3)
        rec_res, _ = self.text_recognizer(image_list)
        return rec_res


class OCRer(object):
    def __init__(self) -> None:
        self.detor = Detector()
        self.recter = Recognizer()

    def predict(self, image_file: str) -> List:
        image = cv2.imread(image_file)
        re_image = cv2.resize(image, dsize=(640, 640), interpolation=cv2.INTER_BITS)
        bboxs = self.detor.predict(re_image)
        blocks = []
        for bbox in bboxs:
            p1 = (int(bbox[0][0]), int(bbox[0][1]))
            p2 = (int(bbox[2][0]), int(bbox[2][1]))
            block = re_image[p1[1] : p2[1], p1[0] : p2[0], :]
            block = cv2.resize(block, dsize=(320, 32), interpolation=cv2.INTER_BITS)
            blocks.append(block)
        output = self.recter.predict(blocks)
        return output


if __name__ == "__main__":
    path = "datas/test.png"
    output = OCRer().predict(path)
    print(output)
