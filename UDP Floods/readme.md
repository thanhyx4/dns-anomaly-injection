"-i", "--input_file"

 "-o", "--output_file"

 "-d", "--duration", default = 60 

  "-z","--num_zombies", default = 1 #default 1 need to specific PortSrcList

"-it", "--initial_time",  default = 0 

"-n", "--num_packet",  default = 5000 

 "-p", "--packets_per_window",  default = 100 
 
 "-w","--window_size", help = 'Window size for server tolerance ( d: 0.01s )', type = float, default = 0.01 
 
"-s","--server_ip", help = "IP address of the target server ( d: )", default = '203.119.73.80' )
 
"-sp", "--sport", help = "Source port ( d: 1280 )", type = int, default = 1280 

 "-sip", "--src_ip", help = "list Source IP ( d: random one )" 

"-ip", "--initial_port", help = "Initial port to attack ( d: 0 )", type = int, default = 0 

"-fp", "--final_port", help = "Final port to attack ( d: 40000 )", type = int, default = 40000 )

"-inp", "--inter_port", help = "Interval between ports ( d: 1 )", type = int, default = 1 )

"-op", "--open_port", help = "Total open ports ( d: random )", type = int )

"-cp", "--closed_port", help = "Total closed ports ( d: random )", type = int )

"-opl", "--open_port_list", help = "List of open ports, ej:1 2 3 ( d: [] )" )

"-cpl", "--closed_port_list", help = "List of closed ports, ejemplo:1 2 3 ( d: [] )" )

"-al", "--activate_icmp_limit", help = "Activate the limit of ICMP responses per second ( Enable to simulate server with Linux or Solaris )", action = "store_true" )

"-il", "--icmp_limit", help = "Limit of ICMP responses per second ( d: 2 )", type = int, default = 2 )
 