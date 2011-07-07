# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Bhaskara Marthi

# Generation of Boost python bindings for ROS messages

from cStringIO import StringIO
from roslib import packages
from roslib import msgs
from roslib import rospack

############################################################
# Main functions
############################################################


def generate_export_function(spec, s):
    "Generate the single helper function that exports the definition of a message type."

    msg = spec.short_name
    s.write("void export{0} ()".format(msg))
    s.write("{")
    with Indent(s, 2):
        s.write("using {0}::{1};".format(spec.package, msg))
        s.write('class_<{0}, shared_ptr<{0}> >("{0}", init<>())'.format(msg))

        array_fields = []

        with Indent(s, 2):
            for field in spec.parsed_fields():
                s.write('.def_readwrite("{0}", &{1}::{0})'.format(field.name, msg))
                if field.is_array:
                    array_fields.append(field)
            s.write(';\n')

        for f in array_fields:
            s.write('class_<vector<{0}> >("{1}_{2}")'.format(qualify(f.base_type),
                                                               msg, f.name))
            with Indent(s, 2):
                s.write('.def(vector_indexing_suite<vector<{0}> > ())'.format(qualify(f.base_type)))
                s.write(';')
    s.write("}\n")


def generate_file(pkg, msg, s=None):
    "Generate the definition file for a single message"
    
    if s is None:
        s = IndentedWriter()
    path = rospack.rospackexec(['find', pkg])
    (_, spec) = msgs.load_from_file("{0}/msg/{1}.msg".format(path, msg), pkg)

    s.write("#include <{0}/{1}.h>".format(pkg, msg))
    s.write("#include <boost/python.hpp>")
    s.write("#include <boost/python/suite/indexing/vector_indexing_suite.hpp>")
    s.write("\n")

    s.write("namespace {0}".format(pkg))
    s.write("{")
    s.write("\n")

    s.write("using namespace boost::python;")
    s.write("using boost::shared_ptr;")
    s.write("using std::vector;")
    s.write("\n")

    generate_export_function(spec, s)

    s.write("} // namespace")

    return s.getvalue()
    
                
############################################################
# Helpers
############################################################

MSG_TYPE_TO_CPP = {'byte': 'int8_t', 'char': 'uint8_t',
                   'bool': 'uint8_t',
                   'uint8': 'uint8_t', 'int8': 'int8_t', 
                   'uint16': 'uint16_t', 'int16': 'int16_t', 
                   'uint32': 'uint32_t', 'int32': 'int32_t',
                   'uint64': 'uint64_t', 'int64': 'int64_t',
                   'float32': 'float',
                   'float64': 'double',
                   'string': 'std::string',
                   'time': 'ros::Time',
                   'duration': 'ros::Duration'}

    
def qualify(name):
    if '/' in name:
        return name.replace('/', '::')
    else:
        return MSG_TYPE_TO_CPP[name]
    

############################################################
# Indented writer
############################################################

class IndentedWriter():

    def __init__(self, s=None):
        self.str = s or StringIO()
        self.indentation = 0
        self.block_indent = False

    def write(self, s, indent=True, newline=True):
        if not indent:
            newline = False
        if self.block_indent:
            self.block_indent = False
        else:
            if newline:
                self.str.write('\n')
            if indent:
                for i in xrange(self.indentation):
                    self.str.write(' ')
        self.str.write(s)

    def newline(self):
        self.str.write('\n')

    def inc_indent(self, inc=2):
        self.indentation += inc

    def dec_indent(self, dec=2):
        self.indentation -= dec

    def reset_indent(self):
        self.indentation = 0

    def block_next_indent(self):
        self.block_indent = True

    def getvalue(self):
        return self.str.getvalue()

class Indent():

    def __init__(self, w, inc=2, indent_first=True):
        self.writer = w
        self.inc = inc
        self.indent_first = indent_first

    def __enter__(self):
        self.writer.inc_indent(self.inc)
        if not self.indent_first:
            self.writer.block_next_indent()

    def __exit__(self, type, val, traceback):
        self.writer.dec_indent(self.inc)


