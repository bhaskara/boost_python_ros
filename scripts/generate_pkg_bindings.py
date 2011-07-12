#!/usr/bin/env python

import roslib
roslib.load_manifest('boost_python_ros')
import sys
import os
import os.path
import boost_python_ros.code_generation as cg
import optparse


if __name__ == "__main__":
    parser = optparse.OptionParser(epilog='Generates boost python bindings for ROS msgs from a particular ROS package.')
    parser.add_option('--package', metavar='ROS_PACKAGE',  dest='package', type='string',
                       help='The ROS package to generate bindings for.')
    parser.add_option('--cpp_target_dir', metavar='CPP_TARGET_DIR', dest='cpp_target_dir', type='string',
                        default= os.getcwd(), help='Where to place the generated cpp files.')
    parser.add_option('--py_target_dir',metavar='PY_TARGET_DIR', dest='py_target_dir', type='string',
                        default= os.getcwd(), help='Where to place the ROS_PACKAGE python converter files.')
    parser.add_option('--current_package', metavar='CURRENT_ROS_PACKAGE', dest='current_package', type='string')
    (options, a) = parser.parse_args()
   
    pkg = options.package
    cpp_target_dir = options.cpp_target_dir
    py_target_dir = options.py_target_dir #os.path.join(args.py_target_dir, pkg)
    if not os.path.exists(py_target_dir):
        os.makedirs(py_target_dir)
    if not os.path.exists(cpp_target_dir):
        os.makedirs(cpp_target_dir)
    cg.write_bindings(pkg, cpp_target_dir)
    cg.write_rospy_conversions(pkg, py_target_dir, options.current_package)
    
