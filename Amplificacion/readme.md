Server tolerance, packets per unit of time that the server can answer, default:100, type=int:
- '-p', '--packets_per_window', 

Fraction of time for server tolerance, default: 0.01, type=float:
- '-w', '--window_size',

Server ip, default: 203.119.73.80
- '-s', '--server_ip'

Source port of the queries, default:21517, type=int.
- '-sp', '--source_port', 

Duration of the attack (seconds), default: 300 sec.
- '-d', '--duration',

Amount of packets per second per zombie, default: 1200', type=int, default=1200)
- '-n', '--num_packets'

Initial time of the attack, default:0', type=float, default=0)
- '-it', '--initial_time'

Response type, true:amplified response, false:normal response. Default: false', action='store_true')
- '-rtype', '--response_type'

Number of computers in the botnet for the DDoS attack, default:1
- '-z', '--zombies'

Required arguments
    
- '-i', '--input_file', help='Path to the input file.', required=True)
    
- '-o','--output_file', help='Path to the output file.',required=True)
    
- '-target', '--target_ip', help= 'Target ip', required=True)
    
- '-dom','--domain', help= 'Asked domain, ex: "niclabs.cl"', required=True)

Set up attack