import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue

def generate_launch_description():	

	# get the required paths of packages & files
	pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
	pkg_mr_robot_desc = get_package_share_directory('mr_robot_description')
	xacro_path = pkg_mr_robot_desc + '/urdf/mr_robot.xacro'
	
    # joint state publisher
	robot_state_publisher = Node(
		        package = 'robot_state_publisher',
				executable = 'robot_state_publisher',
				parameters = [
					    {'robot_description': ParameterValue(Command( \
								['xacro ', os.path.join(pkg_mr_robot_desc, 'urdf/mr_robot.xacro'),
								]), value_type=str)}]
								)
	
    # spawn robot in gz sim using urdf
	spawn_robot = Node(
		        package = "ros_gz_sim",
                executable = "create",
                arguments = ["-topic", "/robot_description",
                                        "-name", "mr_robot",
                                        "-allow_renaming", "true",
                                        "-z", "2.0",
                                        "-x", "0.0",
                                        "-y", "0.0",
                                        "-Y", "-1.57",
                                        ],
							output='screen'
                           )
	return LaunchDescription([
		robot_state_publisher,
		spawn_robot,
    ])