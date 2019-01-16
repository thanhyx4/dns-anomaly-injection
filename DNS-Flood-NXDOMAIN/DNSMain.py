try:
    ##### Sys libraries import and adding the path of modules to use
    import sys
    sys.path.append('..')
    sys.path.append('../RandomSubdomain')
    
    ##### Libraries and module to use, created by us or scapy
    
    from scapy.all import *
    from PacketInserter import *
    from DNSPacketBuilder import *

    ##### Python libraries used
    import time
    import randFloats as rnd
    import randomSubdomain as rndSb
except:

    #### Librarie not found error
    raise Exception("Be sure to have all the libraries installed")


def createFalseDomains(number: int):
    """
        :param number:int: the number of fake domains to make
        :return: a list of false domain names based on the time executed
    """
    domainNames = []
    for i in range(number):
        falseName = rndSb.randomSub()
        falseDomain = falseName+".cl."
        domainNames.append(falseDomain)
    return domainNames


def createPackateNXDomain(srcIp:str,destIp:str,times: list,names: list):
    """
        Creates a list of tuples (request,response) to simulate an NXDOMAIN 
        attack to the DNS server
        :param srcIp:str: the source IP where the attack is generated
        :param destIp:str: the IP of the server
        :param times:list: the time when the attack is given
        :param names:list: the name of the non existant domain
        :return: a list (request,response) of fake queries to be append
    """
    builder = DNSPacketBuilder()
    pkts = []
    for i in range(len(times)):
        idDNS = int(RandShort())
        idQrIp = int(RandShort())
        idRspIp = int(RandShort())
        sport = random.randint(1024,65535)
        packetTime = times[i]
        domainName = names[i]
        z = builder.withSrcIP(srcIp)\
            .withDestIP(destIp)\
            .withSrcPort(sport)\
            .withDestPort(53)\
            .withTime(packetTime)\
            .withDomain(domainName)\
            .withQrIpId(idQrIp)\
            .withRspIpId(idRspIp)\
            .withIdDNS(idDNS)\
            .build()
        pkts.append(z)
    return pkts


def main(args,test=""):
    ##### Reading console input from the user
    inputFileName = args[1]
    attackerIP = args[2]
    if len(args)>=4:
        initialTime = int(args[3])
    else:
        initialTime = 0
    if len(args)>=5:
        atckDuration = int(args[4])
    else:
        atckDuration = 60
    
    ##### Creating the right names for the output file
    fileComponents = inputFileName.split('.pcap')
    outputFileName = fileComponents[0]+"-modified"+test+".pcap"

    ##### Starting the simulation, setting it's parameters
    rate = 2000 ##TODO ver estudios de cuantos son por segundo, por ahora 2000 por segundo it's ok
    first = sniff(offline="input/"+inputFileName,count=1)
    if len(first)== 0:
        ti = initialTime
    else:
        ti=first[0].time + initialTime
    timeOfInsertion = rnd.genInter(time.time(),ti,ti+atckDuration,rate)
    domainNames = createFalseDomains(len(timeOfInsertion))

    ##### Creating the packages and generation it's insertion
    packages = createPackateNXDomain(attackerIP,"200.7.4.7",timeOfInsertion,domainNames)
    inserter = PacketInserter()
    operation = inserter.withPackets(packages)\
                .withInputDir("input/")\
                .withPcapInput(inputFileName)\
                .withOutputDir("output/")\
                .withPcapOutput(outputFileName)\
                .insert()

    ##### Checking if everything goes ok
    if operation:
        print("Packets Inserted")
        return 0
    return 1
#### Runner of the module
if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) == 2:
        arguments.append(0)
        arguments.append(60)
    if len(arguments) == 3:
        arguments.append(60)
    main(arguments)