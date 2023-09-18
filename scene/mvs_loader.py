import numpy as np

def read_camera_parameters(filename):
    with open(filename) as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
    # extrinsics: line [1,5), 4x4 matrix
    extrinsics = np.fromstring(" ".join(lines[1:5]), dtype=np.float32, sep=" ").reshape(
        (4, 4)
    )
    # intrinsics: line [7-10), 3x3 matrix
    intrinsics = np.fromstring(
        " ".join(lines[7:10]), dtype=np.float32, sep=" "
    ).reshape((3, 3))

    params_line = lines[11].split()
    depth_min = float(params_line[0])
    depth_max = float(params_line[-1])
    return intrinsics, extrinsics, depth_min, depth_max
