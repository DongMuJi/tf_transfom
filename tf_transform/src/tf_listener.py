#!/usr/bin/env python  
import rospy
import tf
from std_msgs.msg import Float64MultiArray

if __name__ == '__main__':
    rospy.init_node('tf_listener')

    listener = tf.TransformListener()
    destination_frame = rospy.get_param('/tf_listener/destination_frame','/imu_link')
    original_frame = rospy.get_param('/tf_listener/original_frame','/base_link')
    pub_rate = rospy.get_param('/tf_listener/pub_rate',10)
    pub_topic = rospy.get_param('/tf_listener/pub_topic','/tf_transform/tf_result')

    tf_pub = rospy.Publisher(pub_topic, Float64MultiArray,queue_size=50)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform(destination_frame, original_frame , rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        tf_data = [trans[0],trans[1],trans[2],rot[0],rot[1],rot[2],rot[3]]
        tf_result = Float64MultiArray()
        #print tf_data
        for i in range(len(tf_data)):
            tf_result.data.append(tf_data[i])
        tf_pub.publish(tf_result)
        rate.sleep()
