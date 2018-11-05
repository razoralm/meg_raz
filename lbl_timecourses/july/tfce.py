import numpy
from array import array
import subprocess
import random
import os
import pickle

# check that python outputs data to binary files with expected byte count
assert array("B", [0]).itemsize == 1
assert array("I", [0]).itemsize == 4
assert array("d", [0]).itemsize == 8

def tfce_export_data(A, B, data_filename):
    assert(A.shape == B.shape)
    subject_count = A.shape[0]
    data_length = A.shape[1]

    data_file = open(data_filename, "wb")
    array("I", [subject_count]).tofile(data_file)
    for s in range(A.shape[0]):
        array("I", [data_length]).tofile(data_file)
        array("d", A[s]).tofile(data_file)
        array("I", [data_length]).tofile(data_file)
        array("d", B[s]).tofile(data_file)
    data_file.close()

def tfce_import_result(result_filename):
    # read result back
    result_file = open(result_filename, "rb")
    result_size = array("I", [])
    result_size.fromfile(result_file, 1)
    result = array("B", [])
    result.fromfile(result_file, result_size[0])
    result = result.tolist()
    result_file.close()
    return result

def tfce_1d(A, B, **kwargs):
    # write input data to file
    i = random.randint(0, 1000000)
    data_filename = "/tmp/pytfce-data%06d.bin" % i
    result_filename = "/tmp/pytfce-result%06d.bin" % i
    print("tfce: data filename = {}, result filename = {}".format(data_filename, result_filename))

    tfce_export_data(A, B, data_filename)

    # call libtfce binary
    subprocess.call([
        "/net/server/data/programs/razoral/platon_pmwords/scripts/raz/TFCE_analyses/libtfce",
        "--type", "1d",
        "--input-file", data_filename,
        "--output-file", result_filename,
        "-h", str(kwargs["h"]),
        "-e", str(kwargs["e"]),
        "-n", str(kwargs["n"])
    ])

    # read result back
    # result list contains 1 where difference is significant
    # and 0 where it is not
    return tfce_import_result(result_filename)
