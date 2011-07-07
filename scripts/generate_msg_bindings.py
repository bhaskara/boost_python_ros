#!/usr/bin/env python

import roslib
roslib.load_manifest('boost_python_ros')
import sys
import boost_python_ros.code_generation as cg


if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Usage: {0} PACKAGE MESSAGE".format(sys.argv[0]))
        sys.exit()
    print cg.generate_file(sys.argv[1], sys.argv[2])
    
