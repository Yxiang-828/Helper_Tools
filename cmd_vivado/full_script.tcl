# Interactive Vivado Synthesis Script
# Prompts for project path and automatically detects the top module

puts "Enter the path to the Vivado project file (.xpr):"
gets stdin project_path

# Open the project
open_project $project_path

# Get the top module name from the current fileset
set top_module [get_property top [current_fileset]]

puts "Detected top module: $top_module"

# Synthesis
synth_design -top $top_module -part xc7a35tcpg236-1
write_checkpoint -force ${top_module}_synth.dcp

# Implementation
opt_design
place_design
route_design

# Bitstream generation
write_bitstream -force ${top_module}.bit

# Reports
report_timing_summary -file timing_summary.rpt
report_utilization -file utilization.rpt

# Close project
close_project

puts "Synthesis and implementation completed successfully!"