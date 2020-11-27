from cv2 import cv2
import numpy as np
import time


current_milli_time = lambda: int(round(time.time() * 1000))
itr = lambda: iter(())

def shiftVideo(input, output, pixels):
    frames = []
    cap = cv2.VideoCapture(input)
    frameSize = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    out = cv2.VideoWriter(output, fourcc, int(cap.get(cv2.CAP_PROP_FPS)), frameSize)

    counter = 0

    #initial frames
    print("Loading inital frames.")
    while(counter < int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//pixels)):
        print("Reading frame " + str(counter))
        ret, frame = cap.read()
        frames.append(frame)
        counter += 1

    print("Appended first " + str(counter) + " frames.")

    while(counter < int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        mill = current_milli_time()
        print("Processing " + str(counter-int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//pixels)) + " frame of " + str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)-int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//10))))

        newFrame = itr()
        for frameNumber in range(0, len(frames)):
            newFrame = [*newFrame, *frames[frameNumber][(frameNumber*pixels):(frameNumber*pixels+pixels)]]

        out.write(np.array(newFrame))
        del frames[0]
        ret, frame = cap.read()
        frames.append(frame)
        counter+=1

    print("Finish")
    out.release()
    cap.release()
    cv2.destroyAllWindows()


def waveVideo(input, output, pixels, shift):
   
    frames = []
    cap = cv2.VideoCapture(input)
    frameSize = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    out = cv2.VideoWriter(output, fourcc, int(cap.get(cv2.CAP_PROP_FPS)), frameSize)

    counter = 0

    #initial frames
    print("Loading inital frames.")
    while(counter < shift):
        print("Reading frame " + str(counter))
        ret, frame = cap.read()
        frames.append(frame)
        counter += 1

    print("Appended first " + str(counter) + " frames.")

    while(counter < int(cap.get(cv2.CAP_PROP_FRAME_COUNT)-shift)):
        mill = current_milli_time()
        print("Processing: " + str(counter))
        newFrame = itr()

        mod = 1
        frameNumber = 0
        # print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//pixels))
        for frNum in range(0, int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//pixels)):
            # print(frNum)
            newFrame = [*newFrame, *frames[frameNumber][(frNum*pixels):(frNum*pixels+pixels)]]
            frameNumber+=mod
            if ((frameNumber >= shift-1) | (frameNumber <= 0)):
                mod*=-1
        print(len(np.array(newFrame)))
        print(len(np.array(newFrame)[0]))
        out.write(np.array(newFrame))
        del frames[0]
        ret, frame = cap.read()
        frames.append(frame)
        counter+=1

    print("Finish")
    out.release()
    cap.release()
    cv2.destroyAllWindows()



waveVideo("fight.mp4", "test_out12.mp4", 2, 5)
# shiftVideo("sophiaWavr.mp4", "test_out10.mp4", 20)