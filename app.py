from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import *
import os
import sys
import argparse
from PIL import Image
import cv2
import time

#st.set_page_config(layout = "wide")
st.set_page_config(page_title = "Cattle Detection", page_icon="🐮")

st.markdown(
        """
        <style>
        body {
            background-color: #f8f9fa;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

#################### Title #####################################################
 
st.markdown("<h3 style='text-align: center; color: red; font-family: font of choice, fallback font no1, sans-serif;'>CRL Lab's Cattle Detector</h3>", unsafe_allow_html=True)
st.markdown('#') # inserts empty space
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #868e96; font-size: 12px;'>Developed by CRL Labs, ECED, SVNIT</p>", unsafe_allow_html=True)


#--------------------------------------------------------------------------------

DEMO_VIDEO = os.path.join('data', 'videos', 'sampleVideo0.mp4')

def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)

#---------------------------Main Function for Execution--------------------------

def main():

    source = ("Detect From Video", "Detect From Live Feed")
    source_index = st.sidebar.selectbox("Select Activity", range(
        len(source)), format_func = lambda x: source[x])
    
     
    cocoClassesLst = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
                  "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag",
                  "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
                  "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
                  "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv",
                  "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
                  "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush", "All"]

    # Pre-select indices for "person," "cow," and "horse"
    default_selected_indices = ["cow", "dog", "horse", "person", "car", "motorcycle"]
    dict = {"cow":19, "dog":16, "horse":17, "person":0, "car":2, "motorcycle":3}    

    # Extract keys and values from the dictionary
    keys = list(dict.keys())
    values = list(dict.values())

    classes_index = st.sidebar.multiselect("Select Classes", values,
                                      format_func=lambda x: keys[values.index(x)])
    
    isAllinList = 80 in classes_index
    if isAllinList == True:
        classes_index = classes_index.clear()
        
    print("Selected Classes: ", classes_index)
    
    #################### Parameters to setup ########################################
    # MAX_BOXES_TO_DRAW = st.sidebar.number_input('Maximum Boxes To Draw', value = 5, min_value = 1, max_value = 5)
    deviceLst = ['cpu', '0', '1', '2', '3']
    DEVICES = st.sidebar.selectbox("Select Devices", deviceLst, index = 0)
    print("Devices: ", DEVICES)
    MIN_SCORE_THRES = st.sidebar.slider('Min Confidence Score Threshold', min_value = 0.0, max_value = 1.0, value = 0.4)
    #################### /Parameters to setup ########################################
    
    weights = os.path.join("weights", "yolov5n.pt")
    
    if source_index == 0:
        
        uploaded_file = st.sidebar.file_uploader("Upload Video", type = ['mp4'])
        
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text = 'Resource Loading...'):
                st.sidebar.text("Uploaded Video")
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                data_source = os.path.join("data", "videos", uploaded_file.name)
        
        elif uploaded_file is None:
            is_valid = True
            st.sidebar.text("DEMO Video")
            st.sidebar.video(DEMO_VIDEO)
            data_source = DEMO_VIDEO
        
        else:
            is_valid = False
    
    else:
        ######### Select and capture Camera #################
        
        selectedCam = st.sidebar.selectbox("Select Camera", ("Use WebCam", "Use External Source"), index = 0)
        if selectedCam:
            if selectedCam == "Use External Source":
                data_source = st.sidebar.text_input("Enter the source address", "rtsp://")
                is_valid = True
            else:
                data_source = str(0)
                is_valid = True
        else:
            is_valid = False
        
        st.sidebar.markdown("<strong>Press 'q' multiple times on camera window and 'Ctrl + C' on CMD to clear camera window/exit</strong>", unsafe_allow_html=True)
        
    if is_valid:
        print('valid')
        if st.button('Detect'):
            if classes_index:
                with st.spinner(text = 'Inferencing, Please Wait.....'):
                    detect(weights = weights, 
                        source = data_source,  
                        #source = 0,  #for webcam
                        conf_thres = MIN_SCORE_THRES,
                        #max_det = MAX_BOXES_TO_DRAW,
                        device = DEVICES,
                        save_txt = True,
                        save_conf = True,
                        classes = classes_index,
                        nosave = False, 
                        )
                        
            else:
                with st.spinner(text = 'Inferencing, Please Wait.....'):
                    detect(weights = weights, 
                        source = data_source,  
                        #source = 0,  #for webcam
                        conf_thres = MIN_SCORE_THRES,
                        #max_det = MAX_BOXES_TO_DRAW,
                        device = DEVICES,
                        save_txt = True,
                        save_conf = True,
                    nosave = False, 
                    )
                    
            if source_index == 0:
                with st.spinner(text = 'Preparing Video'):
                    for vid in os.listdir(get_detection_folder()):
                        if vid.endswith(".mp4"):
                            #st.video(os.path.join(get_detection_folder(), vid))
                            #video_file = open(os.path.join(get_detection_folder(), vid), 'rb')
                            #video_bytes = video_file.read()
                            #st.video(video_bytes)
                            video_file = os.path.join(get_detection_folder(), vid)
                            
                stframe = st.empty()
                cap = cv2.VideoCapture(video_file)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                print("Width: ", width, "\n")
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                print("Height: ", height, "\n")

                while cap.isOpened():
                    ret, img = cap.read()
                    if ret:
                        stframe.image(cv2.resize(img, (width, height)), channels = 'BGR', use_column_width = True)
                    else:
                        break
                
                cap.release()
                st.markdown("### Output")
                st.write("Path of Saved Video: ", video_file)    
                st.write("Path of TXT File: ", os.path.join(get_detection_folder(), 'labels'))    
                st.balloons()
            
            else:
                with st.spinner(text = 'Preparing Video'):
                    for vid in os.listdir(get_detection_folder()):
                        if vid.endswith(".mp4"):
                            liveFeedvideoFile = os.path.join(get_detection_folder(), vid)
                    
                    st.markdown("### Output")
                    st.write("Path of Live Feed Saved Video: ", liveFeedvideoFile)    
                    st.write("Path of TXT File: ", os.path.join(get_detection_folder(), 'labels'))    
                    st.balloons()
                


# --------------------MAIN FUNCTION CODE------------------------                                                                    
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
# ------------------------------------------------------------------