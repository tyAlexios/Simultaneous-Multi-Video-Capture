import argparse
import os
import time

import cv2

def make_parser():
    parser = argparse.ArgumentParser("Simultaneous Multi-Video Capture!")

    parser.add_argument(
        "--NumOfCam", type=int, default=0, help="the number of used cameras"
    )
    
    parser.add_argument(
        "--cam1", type=int, default=None, help="webcam demo camera id of view1"
    )

    parser.add_argument(
        "--cam2", type=int, default=None, help="webcam demo camera id of view2"
    )   

    parser.add_argument(
        "--cam3", type=int, default=None, help="webcam demo camera id of view3"
    )

    parser.add_argument(
        "--cam4", type=int, default=None, help="webcam demo camera id of view4"
    )   
    
    return parser

def SaveVideos(n, caps, vid_writers):
    
    frame_id = 0
    frames = []
    
    skip_frames = 30
    
    while True:
        frame_id += 1
        frames.clear()
        flag = True
        for i in range(n):
            ret, frame = caps[i].read()
            flag &= ret
            frames.append(frame)
        
        if frame_id <= skip_frames:
            continue
        
        if not flag:
            print("Cam read error")
            break
        
        for i in range(n):
            cv2.imshow("view{0}".format(i), frames[i])
            vid_writers[i].write(frames[i])
        
        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord("q") or ch == ord("Q"):
            break
        
        
        
def main(args):
    current_time = time.localtime()
    vis_folder = os.path.join("outputs", "track_vis")
    os.makedirs(vis_folder, exist_ok=True)
    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S", current_time)
    save_folder = os.path.join(vis_folder, timestamp)
    os.makedirs(save_folder, exist_ok=True)
    
    NUM_CAM = args.NumOfCam
    
    caps = []
    vid_writers = []
    if args.cam1 is not None:
        caps.append(cv2.VideoCapture(args.cam1))
    if args.cam2 is not None:
        caps.append(cv2.VideoCapture(args.cam2))
    if args.cam3 is not None:
        caps.append(cv2.VideoCapture(args.cam3))
    if args.cam4 is not None:
        caps.append(cv2.VideoCapture(args.cam4))
    
    for i in range(NUM_CAM):
        vid_writers.append( cv2.VideoWriter(
            os.path.join(save_folder, "camera{0}.mp4".format(i)), cv2.VideoWriter_fourcc(*'mp4v'), caps[i].get(cv2.CAP_PROP_FPS), (int(caps[i].get(cv2.CAP_PROP_FRAME_WIDTH)), int(caps[i].get(cv2.CAP_PROP_FRAME_HEIGHT)))
        ))
    
    SaveVideos(NUM_CAM, caps, vid_writers)

if __name__ == "__main__":
    args = make_parser().parse_args()
    main(args)
