# Cattle Detection App with YOLOv5 and Streamlit

## Overview

[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://youtu.be/nPIC4n0p_6k)

This is a cattle detection app that utilizes the YOLOv5 object detection model and is built with Streamlit. The app allows users to perform cattle detection on videos or live camera feed, providing a user-friendly interface for configuring the detection parameters.

## Features

- Object detection using YOLOv5n
- Streamlit-based web application
- Selectable classes for detection
- Supports both video files and live camera feed
- Adjustable confidence score threshold
- Visual output with bounding boxes and labels
- Video output saved for further analysis

## Installation

Follow the steps below to install and run the app on your local machine. You have to follow the **steps 1-4 only once**. After that, you can directly run the app using step 5.

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/cattle-detection-app.git
   cd cattle-detection-app
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv env
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source env/bin/activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## Developed By

This project is developed by CRL Labs, DoECE, SVNIT under the guidance of Dr. S. N. Shah. It was a project developed for Surat Municipal Corporation, by Aditya Kale, Aniket Rana, Manish Lalwani, Ratnadeep Patra.
