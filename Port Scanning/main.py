import argparse
from PackagesCreator import *
import sys
sys.path.append("..")
from PacketInserter import *
from PortsGenerator import *


def main():
    ########################### Valores por defecto ###########################
    Seed=time.time
    attack=[]
    domsFile='ultimos-dominios-1m.txt'
    ###########################################################################
    ###################### Manejo de valores por consola ######################
    parser = argparse.ArgumentParser(description='Port Scanning attack simulator')
    parser.add_argument("-ff", "--final_file", help="Sufijo para el nombre del archivo donde guardar el ataque", default='PortScanningAttack')
    parser.add_argument("-f", "--file", help="Nombre del archivo a procesar, ejemplo: ej.pcap")
    parser.add_argument("-tcp", "--tcp_server_attack", help="Ataque Port Scan tipo TCP SYN al servidor", action="store_true")
    parser.add_argument("-udp", "--udp_server_attack", help="Ataque Port Scan tipo UDP SYN al servidor", action="store_true")
    parser.add_argument("-dom", "--domain_attack", help="Ataque Port Scan tipo UDP SYN al servidor", action="store_true")
    parser.add_argument("-ddos","--ddos_type", help="Extender el ataque a tipo distribuido", action="store_true")
    parser.add_argument("-tz","--total_of_zombies", help="Cantidad de computadores en la botnet para el ataque DDoS (d: 15000)", type=int, default=256)
    parser.add_argument("-ip", "--ip_src", help="Direccion IP de origen (d: 200.27.161.26)", default='200.27.161.26')
    parser.add_argument("-ps", "--sport", help="Puerto de origen (d: 1280)", type=int, default=1280)
    parser.add_argument("-pi", "--iport", help="Puerto menor a atacar (d: 0)", type=int, default=0)
    parser.add_argument("-pf", "--fport", help="Puerto mayor a atacar (d: 1023)", type=int, default=1023)
    parser.add_argument("-inp", "--inter_port", help="Intervarlo entre un puerto y otro (d: 1)", type=int, default=1)
    parser.add_argument("-op", "--open_port", help="Total de puertos abiertos (d: aleatorio)", type=int)
    parser.add_argument("-cp", "--closed_port", help="Total de puertos cerrados (d: aleatorio)", type=int)
    parser.add_argument("-opl", "--open_port_list", help="Lista de puertos abiertos, ejemplo:1 2 3 (d: [])")
    parser.add_argument("-cpl", "--closed_port_list", help="Lista de puertos cerrados, ejemplo:1 2 3 (d: [])")
    parser.add_argument("-s", "--seed", help="Semilla para aleatorizar datos (d: computer time)", type=float)
    parser.add_argument("-d", "--duration", help="Duracion del ataque (d: 60s)", type=float, default=60)
    parser.add_argument("-n", "--num_packages", help="Total de paquetes a enviar (d: 5000)", type=int, default=5000)
    parser.add_argument("-ir", "--int_resp", help="Intervalo de respuesta inicial (d: 0.0001s)", type=float, default=0.0001)
    args = parser.parse_args()

    #################### Manejo de los nombres de archivos ####################
    nombrePktFin=args.final_file
    if nombrePktFin[-5:]=='.pcap':
        nombrePktFin==nombrePktFin[-5:]
    nombrePktIni=args.file
    print("El nombre de archivo a procesar es: ", nombrePktIni)
    index=nombrePktIni.find('.pcap')
    if index==-1:
        print('\nEl nombre del archivo a procesar debe tener una extension valida')
        return
    nombrePktFin=nombrePktIni[:index]+'_'+'nombrePktFin'
    ###########################################################################

    paquete= sniff(offline='input/'+nombrePktIni, count=1)
    tInicial=paquete[0].time #Tiempo de inicio del ataque
    if args.seed:
        Seed=args.seed
    duracion=args.duration
    numPaquetesAEnviar=args.num_packages
    interResp=args.int_resp
    IPsrc=args.ip_src
    totalInfectados=args.total_of_zombies
    PortSrc=args.sport
    #################### Verificacion de valores ingresados ####################
    try:
        assert(len(nombrePktFin)>0 and len(nombrePktIni)>0)
    except:
        raise Exception('Los nombres de archivo no pueden ser vacio')
    try:
        assert('.pcap' in nombrePktIni)
    except:
        raise Exception('Se debe incluir el formato de archivo en el nombre del archivo a abrir')
    try:
        assert(duracion>0)
    except:
        raise Exception('La duracion del ataque debe ser mayor a 0')
    try:
        assert(PortSrc<=65535)
        assert(PortSrc>=0)
    except:
        raise Exception("El puerto de origen debe estar entre 0 y 65535")
    try:
        assert(numPaquetesAEnviar>0)
    except:
        raise Exception("El numero de paquetes a enviar debe ser mayor a 0")
    try:
        assert(interResp>0)
    except:
        raise Exception("El intervalo de respuesta debe ser mayor a 0")
    try:
        assert(len(IPsrc)>=0)
    except:
        raise Exception("La direccion IP no puede ser vacia")
    try:
        assert(totalInfectados>1)
    except:
        raise Exception('La cantidad de computadores zombies debe ser mayor a 1')

    ############################################################################
    ####################### Creacion de puertos a atacar #######################
    if args.udp_server_attack or args.tcp_server_attack:

        puertoInicial=args.iport
        puertoFinal=args.fport
        intervaloPuertos=args.inter_port

    #################### Verificacion de valores ingresados ####################
        try:
            assert(puertoInicial<=65536)
            assert(puertoInicial>=0)
            assert(puertoInicial<=65536)
            assert(puertoInicial>=0)
        except:
            raise Exception("Los puertos deben estar entre 0 y 65535")
        try:
            assert(puertoInicial<=puertoFinal)
        except:
            raise Exception('El puerto menor a atacar debe ser menor que el puerto mayor a atacar')
        try:
            assert(intervaloPuertos>0)
        except:
            raise Exception('El intervalo entre un puerto y otro debe ser mayor a 0')
    ############################################################################
        if args.open_port or args.closed_port:
            if args.open_port:
                print("\nAl ingresar el total de puertos abiertos, el total de puertos cerrados no puede ser modificado")
                abiertos=args.open_port
                puertos=arrayPortsGen(puertoInicial, puertoFinal, intervaloPuertos, abiertos, -1, Seed)
            elif args.closed_port:
                print("\nAl ingresar el total de puertos abiertos, el total de puertos cerrados no puede ser modificado")
                cerrados=args.closed_port
                puertos=arrayPortsGen(puertoInicial, puertoFinal, intervaloPuertos, -1, cerrados, Seed)
        elif args.open_port_list and args.closed_port_list:
            abiertos=string2numList(args.open_port_list, ' ')
            cerrados=string2numList(args.closed_port_list, ' ')
            puertos=[abiertos, cerrados]
        elif args.open_port_list or args.closed_port_list:
            if args.open_port_list:
                abiertos=string2numList(args.open_port_list, ' ')
                puertos=arrayPortsGen(puertoInicial, puertoFinal, intervaloPuertos, abiertos, [], Seed)
            if args.closed_port_list:
                cerrados=string2numList(args.closed_port_list, ' ')
                puertos=arrayPortsGen(puertoInicial, puertoFinal, intervaloPuertos, [], cerrados, Seed)
        else:
            puertos=randomPortsGen(puertoInicial, puertoFinal, intervaloPuertos, Seed)
    ############################################################################

        if args.udp_server_attack:
            if args.ddos_type:
                nombrePktFin=nombrePktFin+'_UDP_DDoS_attack.pcap'
                attack=UDP_DDoS_attack(totalInfectados, puertos, tInicial, tInicial+duracion, numPaquetesAEnviar, Seed, interResp)
            else:
                nombrePktFin=nombrePktFin+'_UDP_attack.pcap'
                attack=UDP_attack(IPsrc, PortSrc, puertos, tInicial, tInicial+duracion, numPaquetesAEnviar, Seed, interResp)
        if args.tcp_server_attack:
            if args.ddos_type:
                nombrePktFin=nombrePktFin+'_TCP_DDoS_attack.pcap'
                attack=TCP_DDoS_attack(totalInfectados, puertos, tInicial, tInicial+duracion, numPaquetesAEnviar, Seed, interResp)
            else:
                nombrePktFin=nombrePktFin+'_TCP_attack.pcap'
                attack=TCP_attack(IPsrc, PortSrc, puertos, tInicial, tInicial+duracion, numPaquetesAEnviar, Seed, interResp)
    elif args.domain_attack:
        if args.ddos_type:
            nombrePktFin=nombrePktFin+'_Domain_DDoS_attack.pcap'
            attack=Domain_DDoS_attack(totalInfectados, tInicial, tInicial+duracion, numPaquetesAEnviar, Seed, interResp)
        else:
            nombrePktFin=nombrePktFin+'_Domain_attack.pcap'
            attack=Domain_attack(IPsrc, PortSrc, tInicial, tInicial+duracion, numPaquetesAEnviar, Seed, interResp)
    else:
        print('Debe seleccionar un tipo de ataque, utilice el comando --help para ver las opciones')
        return
    print('Paquetes de ataque creados exitosamente')
    ins = PacketInserter()
    operation = ins.withPackets(attack)\
                .withInputDir("input/")\
                .withPcapInput(nombrePktIni)\
                .withOutputDir("output/")\
                .withPcapOutput(nombrePktFin)\
                .insert()
    if operation:
        print("Paquetes insertados exitosamente")
    ############################################################################

""" @Javi801
 Gives an array of ints with a given string, transforming the string into a int list

 Params: string -> (str) string to transform
         separador -> (str) string to use as separator between each number

 Return: final -> (list(int)) list of ints in the inicial string
"""
def string2numList(string, separador):
    strList=s.split(separador)
    final=[]
    for i in range(len(strList)):
        if strList[i]=='':
            continue
        num=int(strList[i])
        final+=[num]
    return final

main()
