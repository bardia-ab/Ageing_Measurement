proc program {bit_file} {
	open_hw_manager
	connect_hw_server -url localhost:3121
	current_hw_target [get_hw_targets *]
	open_hw_target
	# Program and Refresh the device
	current_hw_device [lindex [get_hw_devices] 0]
	refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 0]
	set_property PROGRAM.FILE $bit_file [lindex [get_hw_devices] 0]
	#set_property PROBES.FILE {C:/design.ltx} [lindex [get_hw_devices] 0]
	set_param xicom.use_bitstream_version_check false
	program_hw_devices [lindex [get_hw_devices] 0]
	refresh_hw_device [lindex [get_hw_devices] 0]
}

#program "/home/bardia/Desktop/bardia/Timing_Characterization/Data/Bitstreams/[lindex $argv 0].bit"
program "/home/bardia/Desktop/bardia/Timing_Characterization/CR_X2Y1/Bitstreams/[lindex $argv 0].bit"