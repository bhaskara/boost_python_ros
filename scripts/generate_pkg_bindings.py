#!/usr/bin/env python

import roslib
roslib.load_manifest('boost_python_ros')
import sys
import os
import os.path
import boost_python_ros.code_generation as cg
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates boost python bindings for ROS msgs from a particular ROS package.')
    parser.add_argument('--package', metavar='ROS_PACKAGE',  dest='package', type=str,
                       help='The ROS package to generate bindings for.')
    parser.add_argument('--cpp_target_dir', metavar='CPP_TARGET_DIR', dest='cpp_target_dir', type=str, default= os.getcwd(),
                       help='Where to place the generated cpp files.')
    parser.add_argument('--py_target_dir',metavar='PY_TARGET_DIR', dest='py_target_dir', type=str, default= os.getcwd(),
                       help='Where to place the ROS_PACKAGE python converter files.')
    args = parser.parse_args()
   
    pkg = args.package
    cpp_target_dir = args.cpp_target_dir
    py_target_dir = os.path.join(args.py_target_dir, pkg)
    if not os.path.exists(py_target_dir):
        os.makedirs(py_target_dir)
    if not os.path.exists(cpp_target_dir):
        os.makedirs(cpp_target_dir)
    cg.write_bindings(pkg, cpp_target_dir)
    cg.write_rospy_conversions(pkg, py_target_dir)
    
