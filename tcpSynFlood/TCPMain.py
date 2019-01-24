### Imports 
### Of console and system configurations and parser, python main libraries
import sys
import argparse
sys.path.append('..')
import random
import time

### Modules of functions and objects made by us
import randFloats as rnd
import ipGenerator as ipg
from PacketInserter import *
from TCPPacketBuilder import *

### Scapy librarie
from scapy.all import *


def createPackets(fileDirectionName: str,dip: str,number: int,initialTime=0,duration = 1,numberIp = 1):
    """
        Creates a series of packets of information that are going to be added to the pcap file
        :param: fileDirectionName it's the name of the file which is going to be modified with it's direction
        :param dip:str: the destiny IP
        :param number:int: the number per second to create
        :param duration: the duration of the attack on the file
        :return: a list of the packets to insert
    """
    #### First we create a list of random times and the ip's
    first = sniff(offline=fileDirectionName,count=1)
    ti = first[0].time + initialTime
    times =rnd.genInter(time.time(),ti,ti+duration,number)
    print("Creating Ip's of the attack")
    ips = ipg.randomIP(numberIp,time.time(),True)
    #### Then we start to build with our builder
    pktFactory = TCPPacketBuilder()
    pkts = []
    quantity = len(times)
    for i in range(quantity):
        #### Create the random parameters for the attack
        responseTime = abs(random.gauss(0.005931744402515722,0.15624380490520876))
        k = random.randint(0,len(ips)-1)
        sip = ips[k]
        qrIpId = int(RandShort())
        rspIpId = int(RandShort())
        sport = random.randint(1024, 65535)
        packetTime = times[i]
        respTime = packetTime + responseTime
        #### Generate the packages
        npkt = pktFactory.withSrcIP(sip)\
                .withDestIP(dip)\
                .withSrcPort(sport)\
                .withDestPort(53)\
                .withEtherSrc('18:66:da:4d:c0:08')\
                .withEtherResp('18:66:da:e6:36:56')\
                .withFlags('S')\
                .withTime(packetTime)\
                .withIpId(qrIpId)\
                .build()
        rpkt = pktFactory.withSrcIP(dip)\
                .withDestIP(sip)\
                .withSrcPort(53)\
                .withDestPort(sport)\
                .withEtherSrc('18:66:da:e6:36:56')\
                .withEtherResp('18:66:da:4d:c0:08')\
                .withTime(respTime)\
                .withFlags('SA')\
                .withIpId(rspIpId)\
                .build()
        #### Append the packages of request and response on a tuple
        pkts.append((npkt,rpkt))
    return pkts
def main(args,test=""):
    """
    Main function of the program, generates the output file on the
    output folder. 
    :param args:list :  the arguments given by console.
    :param: test: is an extension to the output file name for the test, do not use if
    not testing 
    :return: 0 if everything goes ok!, 1 otherwise
    """
    ##### Reading the inputs from the user
    fileName = args.fileInput
    inputdir = args.inputDirectory
    outputdir = args.outputDirectory
    numberOfIp = args.numberIp
    initialTime = args.ti
    duration = args.duration
    timestamp = args.timestamp
    tolerance = args.tolerance
    pps = args.pps
    despps = args.des
    ##### Generating the files of the output
    destinyIP = "200.7.4.7" #Ip of the server
    direction = inputdir+fileName
    outName = fileName.split(".pcap")
    output = outName[0]+"-modified"+test+".pcap"

    ##### Getting prepared for generating the attack
    number_packets_second = int(abs(random.gauss(pps,despps)))
    while number_packets_second == 0:
        number_packets_second = int(abs(random.gauss(pps,despps)))
    print("Generating attack of "+str(number_packets_second)+" per second")
    pkts=createPackets(direction,destinyIP,number_packets_second,initialTime,duration,numberOfIp)
    print("Number of packets created: "+str(2*len(pkts)))

    ##### Insertion of the packets generated
    print("Inserting packets on the modified pcap")
    ins = PacketInserter()
    operation = ins.withPackets(pkts)\
                .withInputDir(inputdir)\
                .withPcapInput(fileName)\
                .withOutputDir(outputdir)\
                .withPcapOutput(output)\
                .withServerIp("200.7.4.7")\
                .withResponseDt(0.006)\
                .withTimestamp(timestamp)\
                .withServerTolerance(tolerance)\
                .insert()
    ##### Seeing that everything is ok
    if operation:
        print("Packets Inserted")
        return 0
    return 1
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Simulacion de ataque TCP SYN Flood")
    parser.add_argument('-di','--directory_input',dest='inputDirectory',action='store',default='input/',help="Nombre del directorio donde esta el input con / de la ruta",type=str)
    parser.add_argument('-pps','--packetsPerSecond',dest='pps',default=4500,type=int,help="Packets per second of the attack")
    parser.add_argument('-dpps''--desv_packets_per_second',dest='des',default=1000,type=int,help="Standard desviation of the packets per second of the attack")
    parser.add_argument('-fi','--file_input',dest='fileInput',action='store',default='',help="Nombre del archivo pcap con su respesctivas extensiones",type=str)
    parser.add_argument('-ti','--initial_time',dest='ti',action='store',default=0,help='tiempo de inicio del ataque desde el primer paquete del primer archivo',type=int)
    parser.add_argument('-dt','--duration',dest='duration',action='store',default=1,help='tiempo de duracion del ataque, medido en segundos',type=int)
    parser.add_argument('-ipn','--ip_number',dest='numberIp',action='store',default=1,help='cantidad de ips del DDOS, por default es 1',type=int)
    parser.add_argument('-do','--directory_output',dest='outputDirectory',action='store',default='output/',help='direccion del archivo modificado del output',type=str)
    parser.add_argument('-time','--timestamp',dest='timestamp',action='store',default=0.01,help='tiempo de la ventana de medicion, medido en segundos',type=float)
    parser.add_argument('-tol','--tolerance',dest='tolerance',action='store',default=42,help='tolerancia del servidor',type=int)
    arguments = parser.parse_args()
    if arguments.timestamp >= 1.00:
        arguments.timestamp = 1.00
        print("Warning! Changed the timestamp to one second!")
    main(arguments)