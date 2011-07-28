#include <boost/python.hpp>
#include <ros/time.h>
#include <ros/duration.h>


BOOST_PYTHON_MODULE(rostime_boost_python)
{
  using namespace boost::python;
  using boost::shared_ptr;
  using ros::Time;
  using ros::Duration;

  class_<Time, shared_ptr<Time> > ("Time", "Ros time builtin")
    .def_readwrite("sec", &Time::sec)
    .def_readwrite("nsec", &Time::nsec)
    ;

  class_<Duration, shared_ptr<Duration> > ("Duration", "Ros duration builtin")
    .def_readwrite("sec", &Duration::sec)
    .def_readwrite("nsec", &Duration::nsec)
    ;
};
