# FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Update and install tzdata separately
RUN apt update && apt install -y tzdata

RUN apt update \
    && apt install -y \
    nano git wget tmux htop nvtop ninja-build cmake build-essential g++\
    libglew-dev libassimp-dev libboost-all-dev libgtk-3-dev libopencv-dev libglfw3-dev libavdevice-dev libavcodec-dev libeigen3-dev libxxf86vm-dev libembree-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# requirements for headless Open3D rendering
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    libegl1 libgl1 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# image magic is used for resizing in pre process script
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

ENV EGL_PLATFORM surfaceless
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility,graphics
ENV CUDA_HOME /usr/local/cuda-11.8/
ENV TORCH_CUDA_ARCH_LIST="7.0 7.5 8.0 8.6+PTX"
# Install github cli
# RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
#     && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
#     && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
#     && apt update \
#     && apt install -y gh \
#     && rm -rf /var/lib/apt/lists/*


RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user
COPY .devcontainer/.bashrc /home/user/
COPY .devcontainer/.tmux.conf /home/user/
RUN mkdir -p /home/user/workspace

WORKDIR /home/user/workspace
COPY submodules /home/user/workspace/submodules
COPY environment.yml /home/user/workspace/

USER root
RUN chown -R user:user /home/user
USER user

# Install miniconda
WORKDIR /home/user/
ENV CONDA_DIR /home/user/miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /home/user/miniconda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# This makes conda env solving a breeze
RUN conda update -n base conda \
    && conda install -n base conda-libmamba-solver \
    && conda config --set solver libmamba


WORKDIR /home/user/workspace

RUN conda env create --file environment.yml

RUN conda init bash \
    && exec bash \
    && conda activate gaussian_splatting \
    && conda install -c conda-forge -y colmap tensorboard \
    && pip install -y torch-tb-profiler

# Build the viewer now.
# COPY SIBR_viewers /home/user/workspace/SIBR_viewers
# WORKDIR /home/user/workspace/SIBR_viewers
# RUN cmake -Bbuild . -DCMAKE_BUILD_TYPE=Release && \
#     cmake --build build -j24 --target install

# RUN mv ./install/ /home/user/SIBR_viewer
# ENV PATH=/home/user/SIBR_viewer/bin:$PATH

RUN rm -rf /home/user/workspace/
RUN mkdir -p /home/user/workspace

# libs required for X forwarding
USER root
RUN apt update \
    && apt install -y \
    libgl1 \
    libxrender1 \
    libgl1-mesa-glx \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*
USER user


WORKDIR /home/user/workspace/