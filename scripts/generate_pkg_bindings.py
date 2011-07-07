#!/usr/bin/env python

import roslib
roslib.load_manifest('boost_python_ros')
import sys
import os
import boost_python_ros.code_generation as cg


if __name__ == "__main__":
    if len(sys.argv)==2:
        target_dir = os.getcwd()
    elif len(sys.argv)==3:
        target_dir = sys.argv[2]
    else:
        print("Usage: {0} PACKAGE [TARGET_DIR]".format(sys.argv[0]))
        sys.exit()
    cg.write_bindings(sys.argv[1], target_dir)
    
