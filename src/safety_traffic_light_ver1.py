import cv2
import torch
import numpy as np
import time
import serial

# bit info
### b7 b6 b5 b4 b3 b2 b1
###  x  x  x  x en dr dr

# en : traffic light info, 1 -> enable, 0 -> disable
# dr : 00 = off, 01 = up, 10 = down

class VideoFrame(object) :
    FRAME_WIDTH = 0
    FRAME_HEIGHT = 0
    
    def __init__(self, rect_map) :
        self.model = torch.hub.load('ultralytics/yolov5:master', 'yolov5s')
        self.cap = cv2.VideoCapture(0)
        FRAME_WIDTH = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # 640
        FRAME_HEIGHT = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 480
        self.cw_rect = rect_map
        
        self.threshold_line = (self.cw_rect['y1'] + self.cw_rect['y2']) / 2
        
        self.isInRect = lambda x, y : (x > self.cw_rect['x1'] and x < self.cw_rect['x2'] and y > self.cw_rect['y1'] and y < self.cw_rect['y2'])

        self.ret = None
        self.frame = None

    
    def read_frame(self) :
        self.ret, self.frame = self.cap.read()
    
    def entrance_check(self, result_val) :
        detected_obj = self.model(self.frame)
        person_boxes = detected_obj.pred[0][detected_obj.pred[0][:, 5] == 0, :4]
        
        num_people = person_boxes.shape[0]
        person_in_rect = list(filter(lambda i : self.isInRect((i.tolist()[0] + i.tolist()[2]) / 2, (i.tolist()[1] + i.tolist()[3]) / 2), person_boxes))
        
        if len(person_in_rect) == 0 :
            result_val[0] = '0'
            result_val[1] = 0

        elif len(person_in_rect) > 0:
            result_val[1] = 8
            if (person_in_rect[0].tolist()[1] + person_in_rect[0].tolist()[3]) / 2 - self.threshold_line >= 0 :
                result_val[0] = '2'
            else :
                result_val[0] = '1'
        
        print(self.cw_rect, self.threshold_line)
        print("entrance_check : ", num_people, len(person_in_rect), result_val)

    def show(self) :
        frame_with_rect = cv2.rectangle(self.frame, (self.cw_rect['x1'], self.cw_rect['y1']), (self.cw_rect['x2'], self.cw_rect['y2']), (0,255,0), 2)
        cv2.imshow("webcam",frame_with_rect)


class TrafficController(object) :

    def __init__(self) :
        self.serial_port = serial.Serial(port="/dev/ttyUSB0", baudrate = 9600)
        self.video_ctl = VideoFrame({ 'x1' : 105, 'y1' : 130, 'x2' : 450, 'y2' : 380})
        
    def run(self) :
        ans = None
        detection_res = ['0', 0]
        while True:
            print('loop')
            self.video_ctl.read_frame()
            #if self.serial_port.readable() :
            #    ans = self.serial_port.read()
            #print(ans)
            if detection_res[1] == 0 :
                self.video_ctl.entrance_check(detection_res)
            else :
                detection_res[1] -= 1
                time.sleep(0.5)
            print("detection_res : ", detection_res)

            self.serial_port.write(detection_res[0].encode(encoding='ascii'))
            #if (self.serial_port.readable()) :
            #    print("arduino ans : ", self.serial_port.read().decode(encoding='ascii'))
            
            self.video_ctl.show()
            
            if cv2.waitKey(1) == ord('q'):
                break
        self.video_ctl.cap.release()

def main() :
    TrafficController().run()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()
        
