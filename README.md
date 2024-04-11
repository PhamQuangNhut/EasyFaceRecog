<a name="readme-top"></a>


[![LinkedIn][linkedin-shield]][linkedin-url]
[![FaceBook][facebook-shield]][linkedin-url]
[![Gmail][gmail-shield]][gmail-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">EasyFaceRecog</h3>

  <p align="center">
    Utilizing advanced facial recognition technology to streamline and enhance the accuracy of attendance tracking systems.
    <br />
    <a href="https://github.com/PhamQuangNhut/EasyFaceRecog"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/PhamQuangNhut/EasyFaceRecog">View Demo</a>
    ·
    <a href="https://github.com/PhamQuangNhut/EasyFaceRecog">Report Bug</a>
    ·
    <a href="https://github.com/PhamQuangNhut/EasyFaceRecog">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Face recognition technology has become increasingly popular in various applications, including security systems, identity verification, and even attendance management. In this context, a face recognition system for attendance management can streamline the process of marking attendance, making it more efficient and reducing the chances of proxy attendance. This project will leverage Python, a versatile programming language known for its simplicity and powerful libraries, along with Tkinter for creating a graphical user interface (GUI), and DeepFace for the underlying artificial intelligence and face recognition tasks.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

The core of this face recognition for attendance project is built upon a combination of powerful programming languages, frameworks, and libraries. These tools have been carefully selected to ensure the project is both efficient and user-friendly, making it suitable for real-world applications. Below are the key components used in the development of this project:

* [![Python][Python]][Python-url]: As the primary programming language, Python forms the foundation of the project. Known for its simplicity and versatility, Python is widely used in various fields, including data science, web development, automation, and more importantly, artificial intelligence and machine learning. Its extensive libraries and community support make it an ideal choice for building complex applications like this face recognition system.

* [![Tkinter][Tkinter]][Tkinter-url]: Tkinter is the standard GUI library for Python, allowing for the creation of simple to sophisticated graphical user interfaces. It is utilized in this project to design and implement the user interface through which users interact with the system, making the experience seamless and intuitive.

* [![Deepface][Deepface]][Deepface-url]: DeepFace is a lightweight but powerful face recognition and facial attribute analysis framework. It simplifies the integration of advanced AI features into applications, enabling the system to accurately detect and recognize faces in real-time. DeepFace is instrumental in the core functionality of the attendance system, ensuring reliable and efficient face recognition.

* [![OpenCV][OpenCV]][OpenCV-url]: OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. It plays a crucial role in this project by providing a vast range of functionalities for real-time image processing, which is essential for capturing and processing the video feed from the camera for face detection and recognition.

By leveraging these robust frameworks and libraries, the project is well-equipped to handle the complexities of face recognition and attendance management, ensuring a high level of performance and user satisfaction.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This section provides instructions on setting up the project locally.

Setting Up Environment
- Python 3.10
- Conda

**NOTES**
- ⚠️ Commands/Scripts for this project are written for Linux-based OS. They may not work on Windows machines.

### Prerequisites

* 
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/PhamQuangNhut/EasyFaceRecog.git
   ```
2. Install NPM packages
   ```sh
   pip install -r requirements.txt
   ```
3. Enter your database path in `config.py`
   ```python
   - VECTOR_DB_PATH = './DB/emb.npy'
   - SQLITE_DB_PATH = './DB/face_checkin_checkout.DB'
   ```
4. Run the project
   ```python
   - python app.py
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

This project is designed to offer both a detailed analytical view of the face recognition algorithm used for attendance and a practical application for everyday use. Below are the instructions for accessing these features:

Analyzing the Face Recognition Algorithm
For a comprehensive breakdown and interactive exploration of the Face Recognition Algorithm, follow these steps:

1) Ensure that you have Jupyter Notebook installed on your system. If not, you can install it via pip:

   ```pip
   pip install notebook
   ```

2) Navigate to the project's notebook directory from your terminal:
   ```pip
   cd Notebook/
   ```

Running the Face Recognition Attendance Application
To use the face recognition system for attendance management:

1) Navigate to the application directory within your terminal:
   ```pip
   cd App/
   ```
2) Start the application by running the following command:
   ```pip
   python app.py
   ```
   This will activate the GUI, allowing you to interact with the system for registering new users, capturing live attendance through face recognition, and viewing attendance logs.

Ensure all necessary Python dependencies are installed before attempting to run the Notebook or the application. For any issues related to dependencies or execution, please refer to the project's documentation or the 'Installation' section of this README.


<!-- CONTRIBUTING -->
## Fork

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>




## Contact

- Pham Quang Nhut - [@phamnhutcongviec@gmail.com]
- Project Link: [https://github.com/PhamQuangNhut/EasyFaceRecog](https://github.com/PhamQuangNhut/EasyFaceRecog)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments



* [Face Recognition](https://paperswithcode.com/task/face-recognition)
* [Tkinter](https://docs.python.org/3/library/tkinter.htmlt)


<p align="right">(<a href="#readme-top">back to top</a>)</p>




[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/nhut-pham-4a3206301/
[facebook-shield]: https://img.shields.io/badge/-Facebook-black.svg?style=for-the-badge&logo=facebook&colorB=#4267B2
[facebook-url]: https://www.facebook.com/NhutDepTraiProVip/
[gmail-shield]: https://img.shields.io/badge/-Gmail-d14836.svg?style=for-the-badge&logo=gmail&logoColor=white
[gmail-url]: phamnhutcongviec@gmail.com
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-blue?logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Tkinter]: https://img.shields.io/badge/Tkinter-0078D4?&logoColor=white
[Tkinter-url]: https://docs.python.org/3/library/tkinter.html
[DeepFace]: https://img.shields.io/badge/DeepFace-764ABC?&logoColor=white
[DeepFace-url]: https://github.com/serengil/deepface
[OpenCV]: https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/
