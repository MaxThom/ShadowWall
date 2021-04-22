import cv2
import os
from sys import platform
from ctypes import *
import argparse
import sys

# https://github.com/CMU-Perceptual-Computing-Lab/openpose 
# https://github.com/quickgrid/Setup-Guide/blob/master/README.md#windows-10-cmu-openpose-setup-visual-studio-2019-cmake-nvidia-gpu
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#cmake-configuration
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/1_prerequisites.md#windows-prerequisites
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1886
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/01_demo.md
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/advanced/demo_advanced.md
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/02_output.md#ui-and-visual-output
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/advanced/heatmap_output.md
# https://github.com/ankesh007/Body-Measurement-using-Computer-Vision
#
# https://github.com/vladimirvivien/go-cshared-examples#from-python
#
# --display 0
# --disable_blending
#
# [People
#   [Nose[x, y, confidence]
#    Neck[x, y, confidence]]
#    RightShoulder[x, y, confidence]]
#    RightElbow[x, y, confidence]]
#    RightWrist[x, y, confidence]]
#    LeftShould[x, y, confidence]]
#    LeftElbow[x, y, confidence]]
#    LeftWrist[x, y, confidence]]
#    MidHip[x, y, confidence]]
#    RightHip[x, y, confidence]]
#    RightKnee[x, y, confidence]]
#    RightAnkle[x, y, confidence]]
#    LeftHip[x, y, confidence]]
#    LeftKnee[x, y, confidence]]
#    LeftAnkle[x, y, confidence]]
#    RightEye[x, y, confidence]]
#    LeftEye[x, y, confidence]]
#    RightEar[x, y, confidence]]
#    LeftEar[x, y, confidence]]
#    LeftBigToe[x, y, confidence]]
#    LeftSmallToe[x, y, confidence]]
#    LeftHeel[x, y, confidence]]
#    RightBigToe[x, y, confidence]]
#    RightSmallToe[x, y, confidence]]
#    RightHeel[x, y, confidence]]
#    Background[x, y, confidence]]
#   ]
# ]
#

def display(datums):
    datum = datums[0]
    cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
    key = cv2.waitKey(1)
    return (key == 27)


def printKeypoints(datums):
    datum = datums[0]
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    print("Face keypoints: \n" + str(datum.faceKeypoints))
    print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
    print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '\..\openpose\python\openpose\Release');
            print(dir_path + '\..\openpose\python\openpose\Release')
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '\..\openpose\\release;' +  dir_path + '\..\openpose\\bin;'
            print(dir_path + '\..\openpose\\release;' +  dir_path + '\..\openpose\\bin;')
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-display", action="store_true", help="Disable display.")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = dir_path + "\..\openpose\models\\"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython(op.ThreadManagerMode.AsynchronousOut)
    opWrapper.configure(params)
    opWrapper.start()

    # Main loop
    userWantsToExit = False
    while not userWantsToExit:
        # Pop frame
        datumProcessed = op.VectorDatum()
        if opWrapper.waitAndPop(datumProcessed):
            if not args[0].no_display:
                # Display image
                userWantsToExit = display(datumProcessed)
            printKeypoints(datumProcessed)
        else:
            break
    
except Exception as e:
    print(e)
    sys.exit(-1)
