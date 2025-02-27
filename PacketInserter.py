from scapy.all import *
import math
import sys
import states.InserterState as state
import gzip


"""
Packet inserter, inserts packets for the attack simulation
and creates a new pcap file with the attacks given.
@author: Joaquin Cruz
"""
class PacketInserter:
    def __init__(self):
        """
            Creates a default packet inserter.
            :param: packetsToAppend is the tuple (request,response) list for the packets that
            will be added to the pcap file
            :param: input is the name of the pcap file with it's extension
            :param: output is the of the output pcap file with it's extension
            :param: serverIp is the ip of the server to be attacked
            :param: state is the state of the server simulated
            :param: responseDt is the difference of time to be applied on the response of the server
            :param: args is the arguments of the function to create packets
            :param: quantity is the number of arguments to read when creating the packets
            :param: timestamp is the time period where the buffer will be measuring
            :param: serverTolerance is the number of querie's by the timestamp defined that the server
                                    can handle
        """
        self.__quantity = 100
        self.__args=[]
        self.__packetsToAppend=[]
        self.__input=""
        self.__output=""
        self.__serverIp = "200.7.4.7"
        self.__responseDt= 0.006
        self.__state = state.ReadOkState(self)
        self.__timestamp = 0.01
        self.__serverTolerance = 100
    def getTimestamp(self):
        """
            Getter for the timestamp field of the object
            :return: the timestamp defined on in an object instance
        """
        return self.__timestamp
    def getServerTolerance(self):
        """
            Getter for the server tolerance
            :return: the server tolerance
        """
        return self.__serverTolerance
    def changeState(self,anotherState):
        """
            Changes the state that the inserter currently have for
            another new state.
            :param: anotherState is the new state of the inserter
        """
        self.__state = anotherState
    def getPacketsToAppend(self):
        """
            Getter for the packet list
        """
        return self.__packetsToAppend
    def getInputName(self):
        """
            Getter for the input file name
        """
        return self.__input
    def getOutputName(self):
        """
            Getter for the output file name field
        """
        return self.__output
    def getResponseDt(self):
        """
            Getter for delay of the response number
        """
        return self.__responseDt
    def getServerIp(self):
        """
            Get the server Ip to see what packets are response one's
            :return: the ip of the server set
        """
        return self.__serverIp
    def getState(self):
        """
            Getter for the currently state of the inserter.
            :return: the current state
        """
        return self.__state
    def withPackets(self,packets: list):
        """
            Sets the list to packets to be inserted in the pcap file,
            it has to be a list of tuples (request,response).
            :param packets:list: the list of packets that will be inserted
            :return: a reference to the object
        """
        self.__packetsToAppend = packets
        return self
    def withPcapInput(self,input: str):
        """
            Defines the input file that is going to be given
            :param input:str: the name with the extension of the input file
            :return: a reference to the inserter
        """
        self.__input=input
        return self
    def withPcapOutput(self,output: str):
        """
            Establishes the output pcap file name, has to be with the .pcap extension
            :param output:str:
            :return: a reference to the inserter
        """
        self.__output=output
        return self
    def withServerIp(self,ip: str):
        """
            Setter for the server ip for the delay
            :param: ip: str: the ip of the server
        """
        self.__serverIp = ip
        return self
    def withResponseDt(self,dt: float):
        """
            Setter for the request response dt, base it calculation for the delay time
        """
        self.__responseDt = dt
        return self
    def withTimestamp(self, timestamp: float):
        """
            Setter for the server timestamp, this is, the number of seconds that the medition for the
            server tolerance will have. For example, if the timestamp is 0.01, the buffers on the inserter will
            get only packets of a time interval of timestamp seconds. It have to be measured in seconds
        """
        self.__timestamp = timestamp
        return self
    def withServerTolerance(self, tolerance: int):
        """
            Setter for the server tolerance, this is, given the timestamp of the medition, the server can
            receive a maximum number of tolerance queries in that timestamp.
            For example, if the timestamp is 0.01 seconds and the tolerance is 30, the server can't get more than
            30 queries in 0.01 seconds of data analisis.
            :param: tolerance: int: maximum number of queries that the server can get in the timestamp given
        """
        self.__serverTolerance = tolerance
        return self
    def withArgs(self,args: list):
        """
            Establishes the arguments of the function for creating the packets.
            :param: args: list: a matrix of arguments to give it to the function that create the packets
        """
        self.__args = args
        return self
    def withQuantity(self,quantity: int):
        """
            Establishes the quantity of arguments to read when the inserter querie for creating the packets
            :param: quantity: int: the number of arguments to
        """
        self.__quantity = quantity
        return self
    def _calculateDelay(self,pktsPerSecond: float):
        """
            Calculates the time to add for the delay given the response dt.
            :return: the time of delay of the packet
        """
        porcentage = 0
        if pktsPerSecond >= 1000:
            porcentage = 0.5
        if pktsPerSecond >= 2000:
            porcentage = 0.8
        if pktsPerSecond >= 3000:
            porcentage = 1.5
        if pktsPerSecond >= 4000:
            porcentage = 1.7
        if pktsPerSecond >= 5000:
            porcentage = 2.3
        delay = self.__responseDt * porcentage
        return delay
    def insert(self,f):
        """
            Insert the packages given to the pcap file mentioned, (if the output
            file exists already, it will be overwritten)
            from the pcap original file. At the end, the list to append will be empty, so be careful. Also, generate
            packets in order to inser to the attack, it does a querie to the f function to create the package while the
            arguments field of the inserter is not empty
            :param: f: a function to create the packets, it must receive a list
            :return: True if the file was succesfully generated, False if a problem happened
        """
        assert self.__input != self.__output
        try:
            #### Preparing the buffers for insertion
            buffer = [] # normal buffer for the reader of the file
            bufferResponse = [] # buffer for the responses
            bufferQueries = [] # buffer for the queries
            noResponse = {} # dictionary for the queries with no responses
            #### Preparing the delay variables
            ti = 0 #Number of second passed from the first querie readed
            ta = ti #Time of the last package received
            queries = 0 # number of queries without response

            #### Preparing variables to insert the packets
            inputDirection = self.__input
            outputDirection = self.__output
            count = 0 #Counter, resets the writer in order to not persue a memory failure of writing
            wrpcap(outputDirection,PacketList()) #Cleans the pcap output file.
            reader = PcapReader(inputDirection)
            writer = PcapWriter(outputDirection,append=True,sync=True)

            try:
                first = reader.read_packet()        #read till the end
            except EOFError:
                print("Error file pcap doesnt contain packets")
                return False
            ti = first.time
            ta = ti
            buffer.append(first)
            self.__packetsToAppend = [] ## buffer for the attack packets of it's attack
            i = 0
            #### Loop for the slow reading and writing of the packet
            while True:
                if len(self.__args) != 0 and len(self.__packetsToAppend) == 0:
                    while len(self.__args) != 0 and i < self.__quantity:
                        pkts = f(self.__args[0])
                        del self.__args[0]
                        # if len(pkts) <= 2:                          #check list pkts: from build packet (requestPacket, responsePacket) before append
                        #     print(len(pkts))
                        #     print(pkts)
                        #     self.__packetsToAppend.append(pkts)
                        # else:
                        #
                        #     self.__packetsToAppend += pkts
                        self.__packetsToAppend += pkts
                        i+=1
                    i = 0

                #### Calculating the delay of the response
                dt = math.ceil(ta-ti)
                if dt == 0:
                    dt = 1
                pps = queries/dt
                delay = self._calculateDelay(pps)

                #### Reading one packet from the original file
                try:
                    pktRead = reader.read_packet()
                except EOFError:
                    pktRead = None
                #### Checking the condition to reset the writer for overflow bug or
                #### ending the loop
                if pktRead == None:
                    break
                #### Processing the data readed and their value.
                buffer.append(pktRead)
                (count,queries,ta,writer) = self.__state.processData(buffer,self.__packetsToAppend,bufferQueries,bufferResponse,noResponse,delay,[count,queries,outputDirection], writer)
            print("Original File processed")
            ## We have readed all the pcap, we eliminate the reader resources
            reader.close()
            del reader
            if len(self.__args) != 0 and len(self.__packetsToAppend) == 0:
                while len(self.__args) != 0 and i < self.__quantity:
                    pkts = f(self.__args[0])
                    del self.__args[0]
                    # if len(pkts) <= 2:
                    #     self.__packetsToAppend.append(pkts)
                    # else:
                    #     self.__packetsToAppend += pkts
                    self.__packetsToAppend += pkts
                    i+=1
                i = 0
            ### Processing the data that have not been written on the pcap file and it's still in the buffer
            while len(buffer) != 0 and len(self.__args) != 0:
                if len(self.__packetsToAppend) == 0:
                    while len(self.__args) != 0 and i < self.__quantity:
                        pkts = f(self.__args[0])
                        del self.__args[0]
                        # if len(pkts) <= 2:
                        #     self.__packetsToAppend.append(pkts)
                        # else:
                        #     self.__packetsToAppend += pkts
                        self.__packetsToAppend += pkts
                        i+=1
                    i = 0
                dt = math.ceil(ta-ti)
                if dt == 0:
                    dt = 1
                pps = queries / dt
                delay = self._calculateDelay(pps)
                (count,queries,ta,writer) = self.__state.processData(buffer,self.__packetsToAppend,bufferQueries,bufferResponse,noResponse,delay,[count,queries,outputDirection], writer)
            ### Checking if some buffer it's not emptied
            while len(buffer) != 0:
                dt = math.ceil(ta-ti)
                if dt == 0:
                    dt = 1
                pps = queries / dt
                delay = self._calculateDelay(pps)
                (count,queries,ta,writer) = self.__state.processData(buffer,self.__packetsToAppend,bufferQueries,bufferResponse,noResponse,delay,[count,queries,outputDirection], writer)
            while len(self.__args) !=0:
                while i < self.__quantity:
                    pkts = f(self.__args[0])
                    del self.__args[0]
                    # if len(pkts) <= 2:
                    #     self.__packetsToAppend.append(pkts)
                    # else:
                    #     self.__packetsToAppend += pkts
                    self.__packetsToAppend += pkts
                    i+=1
                i = 0
            while len(self.__packetsToAppend) != 0:
                dt = math.ceil(ta-ti)
                if dt == 0:
                    dt = 1
                pps = queries / dt
                delay = self._calculateDelay(pps)
                (count,queries,ta,writer) = self.__state.processData(buffer,self.__packetsToAppend,bufferQueries,bufferResponse,noResponse,delay,[count,queries,outputDirection], writer)
            print("Buffers of packets ready")
            ## Writing on the file of the buffers needed
            while len(bufferQueries) != 0 and len(bufferResponse) != 0:
                if count == 50000:
                    writer.close()
                    del writer
                    writer = PcapWriter(outputDirection,append = True, sync = True)
                    count = 0
                if bufferQueries[0].time < bufferResponse[0].time:
                    writer.write(bufferQueries[0])
                    del bufferQueries[0]
                    count +=1
                else:
                    writer.write(bufferResponse[0])
                    del bufferResponse[0]
                    count +=1
            while len(bufferQueries) != 0:
                if count == 50000:
                    writer.close()
                    del writer
                    writer = PcapWriter(outputDirection,append = True, sync = True)
                    count = 0
                writer.write(bufferQueries[0])
                del bufferQueries[0]
                count+=1
            while len(bufferResponse) != 0:
                if count == 50000:
                    writer.close()
                    del writer
                    writer = PcapWriter(outputDirection,append = True,sync = True)
                    count = 0
                writer.write(bufferResponse[0])
                del bufferResponse[0]
                count += 1

            #### We close the writer and return true because everything goes as planned
            writer.close()
            in_file = outputDirection
            out_file = outputDirection + ".gz"
            in_data = open(in_file,'rb').read()
            gzf = gzip.open(out_file,'wb')
            gzf.write(in_data)
            gzf.close()
            return True
        except FileNotFoundError:
            #### If the file does not exist, we return false because something went wrong
            print("Error file not found")
            return False
