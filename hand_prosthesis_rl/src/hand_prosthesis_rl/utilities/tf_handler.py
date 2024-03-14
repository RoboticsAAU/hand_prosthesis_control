import rospy
import numpy as np
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PoseStamped

class TFHandler():
    def __init__(self):        
        # Initialize the TF2 buffer and listener. The buffer will store the latest transforms
        # and the listener will listen for new transforms and update the buffer.
        self._tf_buffer = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer)
    
    def get_transform(self, child_frame_id : str, parent_frame_id : str = "world") -> TransformStamped:
        """
        It will get the transform from the parent_frame_id to the child_frame_id.
        :param parent_frame_id: The parent frame id (default is "world")
        :param child_frame_id: The child frame id
        :return: The transform
        """
        try:
            return self._tf_buffer.lookup_transform(child_frame_id, parent_frame_id, rospy.Time(0))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            rospy.logwarn("Failed to get transform: %s", str(e))
            return None
    
    def transform_pose(self, input_pose, target_frame : str):
        """
        It will transform the input_pose to the target_frame.
        :param input_pose: The input pose
        :param target_frame: The target frame
        :return: The transformed pose
        """
        try:
            return self._tf_buffer.transform(input_pose, target_frame, rospy.Duration(1))
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            rospy.logwarn("Failed to transform pose: %s", str(e))
            return None
