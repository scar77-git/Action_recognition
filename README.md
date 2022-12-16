# Action_recognition:

Run the folllowing commands to install all the packages:
pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cu102

pip install 'git+https://github.com/facebookresearch/fvcore'

pip install opencv-python

pip install -U iopath

pip install psutil

pip install tensorboard

pip install moviepy

pip install 'git+https://github.com/facebookresearch/fairscale'

pip install av

pip install simplejson

pip install "git+https://github.com/facebookresearch/pytorchvideo.git"

pip install -U 'git+https://github.com/facebookresearch/fvcore.git' 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

git clone https://github.com/facebookresearch/detectron2 detectron2_repo

pip install -e detectron2_repo

git clone https://github.com/SibiAkkash/SlowFast.git

export PYTHONPATH=/path/to/SlowFast/slowfast:$PYTHONPATH

cd SlowFast

python setup.py build develop

Run this to get inference:

python tools/run_net.py --cfg configs/Kinetics/SLOWFAST_8x8_R50.yaml TEST.ENABLE False TRAIN.ENABLE False DEMO.ENABLE True TENSORBOARD.MODEL_VIS.ENABLE True NUM_GPUS 1 TEST.CHECKPOINT_FILE_PATH   DEMO.INPUT_VIDEO  DEMO.OUTPUT_FILE  DEMO.LABEL_FILE_PATH 
