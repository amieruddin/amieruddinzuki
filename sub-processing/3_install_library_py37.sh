#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

#all this local library are for python version 3.8
#--------------------------------------------------------------------------------
# to uninstall all library package in venv
# pip freeze > requirements.txt
# pip uninstall -r requirements.txt 		#remove one by one
# pip uninstall -r requirements.txt -y 	#remoe all at once



#--------------------------------------------------------------------------------
# below are all library needed including its dependency


#--------------------------------------------------------------------------------
#delete previos env and all library in it
#make sure (base) appears at front of terminal

#conda deactivate
#conda env remove --name toll_env

# create new env with python 3.7
#conda create --name toll_env python=3.7 -y

#---------------------------------------------------------------------------------


#activate toll_env 
source toll_env

#matplotlib and its dependencies

echo -e "${bold}\nInstalling : six${normal}"
pip install six-1.16.0-py2.py3-none-any.whl

echo -e "${bold}\nInstalling : pyparsing${normal}"
pip install pyparsing-3.0.4-py3-none-any.whl

echo -e "${bold}\nInstalling : numpy${normal}"
pip install numpy-1.19.1-cp37-cp37m-manylinux2010_x86_64.whl

echo -e "${bold}\nInstalling : python_dateutil${normal}"
pip install python_dateutil-2.8.2-py2.py3-none-any.whl

echo -e "${bold}\nInstalling : Pillow${normal}"
pip install Pillow-9.2.0-cp37-cp37m-manylinux_2_28_x86_64.whl

echo -e "${bold}\nInstalling : cycler${normal}"
pip install cycler-0.11.0-py3-none-any.whl

echo -e "${bold}\nInstalling : kiwisolver${normal}"
pip install kiwisolver-1.3.1-cp37-cp37m-manylinux1_x86_64.whl

echo -e "${bold}\nInstalling : matplotlib${normal}"
pip install matplotlib-3.3.4-cp37-cp37m-manylinux1_x86_64.whl


#PyYAML
echo -e "${bold}\nInstalling : PyYAML${normal}"
pip install PyYAML-5.4.1-cp37-cp37m-manylinux1_x86_64.whl


#matplotlib and its dependencies

echo -e "${bold}\nInstalling : idna${normal}"
pip install idna-3.3-py3-none-any.whl

echo -e "${bold}\nInstalling : urllib3${normal}"
pip install urllib3-1.26.7-py2.py3-none-any.whl

echo -e "${bold}\nInstalling : certifi${normal}"
pip install certifi-2022.6.15.2-py3-none-any.whl

echo -e "${bold}\nInstalling : charset_normalizer${normal}"
pip install charset_normalizer-2.0.4-py3-none-any.whl

echo -e "${bold}\nInstalling : requests${normal}"
pip install requests-2.27.1-py2.py3-none-any.whl



#for setting gui need install pyqt5 and chime
echo -e "${bold}\nInstalling : chime${normal}"
pip install chime-0.5.3-py3-none-any.whl

echo -e "${bold}\nInstalling : PyQt5${normal}"
pip install PyQt5-5.15.7-cp37-abi3-manylinux1_x86_64

echo -e "${bold}\nInstalling : PyQt5-Qt5${normal}"
pip install PyQt5_Qt5-5.15.2-py3-none-manylinux2014_x86_64.whl

echo -e "${bold}\nInstalling : PyQt5-sip${normal}"
pip install PyQt5_sip-12.11.0-cp37-cp37m-manylinux1_x86_64.whl





#scipy
echo -e "${bold}\nInstalling : scipy${normal}"
pip install scipy-1.5.2-cp37-cp37m-manylinux1_x86_64.whl

#tqdm
echo -e "${bold}\nInstalling : tqdm${normal}"
pip install tqdm-4.62.3-py2.py3-none-any.whl

#pytz dependencies
echo -e "${bold}\nInstalling : pytz${normal}"
pip install pytz-2020.1-py2.py3-none-any.whl


#pandas
echo -e "${bold}\nInstalling : pandas${normal}"
pip install pandas-1.1.3-cp37-cp37m-manylinux1_x86_64.whl


#seaborn
echo -e "${bold}\nInstalling : seaborn${normal}"
pip install seaborn-0.11.2-py3-none-any.whl


#psutil
echo -e "${bold}\nInstalling : psutil${normal}"
pip install psutil-5.8.0-cp37-cp37m-manylinux2010_x86_64.whl


#opencv-python
echo -e "${bold}\nInstalling : opencv-python${normal}"
pip install opencv_python-4.1.0.25-cp37-cp37m-manylinux1_x86_64.whl


#torch and it dependencies

echo -e "${bold}\nInstalling : typing_extensions${normal}"
pip install typing_extensions-4.1.1-py3-none-any.whl

echo -e "${bold}\nInstalling : torch${normal}"
pip install torch-1.12.0+cu116-cp37-cp37m-linux_x86_64.whl

echo -e "${bold}\nInstalling : torchvision${normal}"
pip install torchvision-0.13.0+cu116-cp37-cp37m-linux_x86_64.whl

echo -e "${bold}\nInstalling : torchaudio${normal}"
pip install torchaudio-0.12.0+cu116-cp37-cp37m-linux_x86_64.whl




#flask and it dependencies

echo -e "${bold}\nInstalling : MarkupSafe${normal}"
pip install MarkupSafe-2.1.1-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

echo -e "${bold}\nInstalling : zipp${normal}"
pip install zipp-3.8.1-py3-none-any.whl

echo -e "${bold}\nInstalling : itsdangerous${normal}"
pip install itsdangerous-2.1.2-py3-none-any.whl

echo -e "${bold}\nInstalling : Werkzeug${normal}"
pip install Werkzeug-2.2.2-py3-none-any.whl

echo -e "${bold}\nInstalling : Jinja2${normal}"
pip install Jinja2-3.1.2-py3-none-any.whl

echo -e "${bold}\nInstalling : importlib_metadata${normal}"
pip install importlib_metadata-4.12.0-py3-none-any.whl

echo -e "${bold}\nInstalling : click${normal}"
pip install click-8.0.3-py3-none-any.whl

echo -e "${bold}\nInstalling : Flask${normal}"
pip install Flask-2.2.2-py3-none-any.whl



#waitress

echo -e "${bold}\nInstalling : waitress${normal}"
pip install waitress-2.1.2-py3-none-any.whl


#cryptography and it dependencies

echo -e "${bold}\nInstalling : pycparser${normal}"
pip install pycparser-2.21-py2.py3-none-any.whl

echo -e "${bold}\nInstalling : cffi${normal}"
pip install cffi-1.14.6-cp37-cp37m-manylinux1_x86_64.whl

echo -e "${bold}\nInstalling : cryptography${normal}"
pip install cryptography-38.0.1-cp36-abi3-manylinux_2_28_x86_64.whl




#installing tensorrt and it dependencies

echo -e "${bold}\nInstalling : nvidia_cudnn_cu11${normal}"
pip install nvidia_cudnn_cu11-8.5.0.96-py3-none-manylinux1_x86_64.whl

echo -e "${bold}\nInstalling : nvidia_cuda_runtime_cu11${normal}"
pip install nvidia_cuda_runtime_cu11-11.7.99-py3-none-manylinux1_x86_64.whl

echo -e "${bold}\nInstalling : nvidia_cublas_cu11${normal}"
pip install nvidia_cublas_cu11-11.10.3.66-py3-none-manylinux1_x86_64.whl

echo -e "${bold}\nInstalling : nvidia_tensorrt${normal}"
pip install nvidia_tensorrt-8.4.1.5-cp37-none-manylinux_2_17_x86_64.whl


#ONNX and it dependencies

echo -e "${bold}\nInstalling : protobuf${normal}"
pip install protobuf-3.19.4-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

echo -e "${bold}\nInstalling : onnx${normal}"
pip install onnx-1.11.0-cp37-cp37m-manylinux_2_12_x86_64.manylinux2010_x86_64.whl


#----------------------------------------------------------------------

# 2 ways to install cuda toolkit

#1 install cuda toolkit 11.6 using runfile(local)
#echo -e "${bold}\nInstalling : CUDA 11.6${normal}"
#sudo cp /media/delloyd/VAVC_KESAS_1/installation_tol/py37/cuda_toolkit/cuda_11.6.0_510.39.01_linux.run /media/delloyd/VAVC_KESAS_1/installation_tol/py37
#sudo sh cuda_11.6.0_510.39.01_linux.run
#sudo rm /home/delloyd/install_library_local/cuda_11.6.0_510.39.01_linux.run


#2 install cuda toolkit using deb(local)
#required internet

#echo -e "${bold}\nInstalling : CUDA Toolkit - using deb(local)${normal}"
#echo -e "${bold}Make sure internet connection establish\n${normal}"
#echo "copying CUDA file..."
#sudo cp /home/delloyd/install_library_local/cuda_toolkit/cuda-ubuntu2004.pin /home/delloyd/install_library_local
#sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600

#sudo cp /home/delloyd/install_library_local/cuda_toolkit/cuda-repo-ubuntu2004-11-6-local_11.6.0-510.39.01-1_amd64.deb /home/delloyd/install_library_local
#sudo dpkg -i cuda-repo-ubuntu2004-11-6-local_11.6.0-510.39.01-1_amd64.deb
#sudo apt-key add /var/cuda-repo-ubuntu2004-11-6-local/7fa2af80.pub
#sudo apt-get update
#sudo apt-get -y install cuda
#sudo rm /home/delloyd/install_library_local/cuda-repo-ubuntu2004-11-6-local_11.6.0-510.39.01-1_amd64.deb


# sudo reboot







#echo -e "${bold}\nInstalling : scipy${normal}"
#pip install 

