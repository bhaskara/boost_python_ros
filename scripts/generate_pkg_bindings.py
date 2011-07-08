#!/usr/bin/env python

import roslib
roslib.load_manifest('boost_python_ros')
import sys
import os
import os.path
import boost_python_ros.code_generation as cg


if __name__ == "__main__":
    if len(sys.argv)==2:
        base_dir = os.getcwd()
    elif len(sys.argv)==3:
        base_dir = sys.argv[2]
    else:
        print("Usage: {0} PACKAGE [TARGET_DIR]".format(sys.argv[0]))
        sys.exit()

    pkg = sys.argv[1]
    cpp_target_dir = base_dir
    py_target_dir = os.path.join(base_dir, pkg)
    if not os.path.exists(py_target_dir):
        os.makedirs(py_target_dir)
    
    cg.write_bindings(pkg, cpp_target_dir)
    cg.write_rospy_conversions(pkg, py_target_dir)
    
