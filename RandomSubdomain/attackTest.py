import unittest
from randomSubdomain import *

class attackTest(unittest.TestCase):
    def setUp(self):
        self.src_ip = "8.8.8.8"
        self.serv = "200.7.4.7"
        self.dom = "hola.cl"
        self.dom_ip = genIp()
        self.snd_ip = genIp()
        self.d = 20
        self.c = 300
        self.ti = 10
        self.src_port = 31456
        self.packets = randomSubAttack(self.src_ip, self.serv, self.dom, self.dom_ip, self.snd_ip, self.d, self.c, self.ti, self.src_port)
        self.tuples = self.c * self.d
        self.npackets = self.tuples * 2

    def test_attack_number_generated_packets(self):
        self.assertEqual(len(self.packets), self.tuples, "Wrong number of generated tuples")
        n_packets = 0
        n_req = 0
        n_res = 0
        for t in self.packets:
            for p in t:
                n_packets += 1
                if(p[DNS].qr == 0):
                    n_req += 1
                else:
                    n_res += 1
        self.assertEqual(n_packets, self.npackets, "Wrong number of generated packets")
        self.assertEqual(n_req, self.d * self.c, "Wrong number of generated requests")
        self.assertEqual(n_res, self.d * self.c, "Wrong number of generated responses")

    def test_attack_structure(self):
        for t in self.packets:
            self.assertEqual(len(t), 2, "Len of tuples must be 2")
            p0 = t[0]
            p1 = t[1]
            self.assertEqual(p0[DNS].qr, 0, "Structure must be (request, response)")
            self.assertEqual(p1[DNS].qr, 1, "Structure must be (request, response)")


    def test_attack_time(self):
        ti = self.packets[0][0].time
        tf = self.packets[len(self.packets) - 1][0].time
        self.assertTrue(abs(ti - self.ti) <= 1, "Wrong initial time")
        self.assertTrue(self.ti < ti, "Wrong initial time")
        self.assertTrue(abs(tf - self.ti - self.d) <= 1, "Wrong last packet arrival time")
        self.assertTrue(tf < self.ti + self.d, "Wrong last packet arrival time")

    def test_attack_packet_structure(self):
        for t in self.packets:
            req = t[0]
            res = t[1]

            self.assertEqual(res[DNS].rcode, 0, "DNS rcode must be 0")
            self.assertEqual(res[DNS].id, req[DNS].id, "Wrong response DNS id")
            self.assertEqual(res[DNS].qd, req[DNS].qd, "Is answering a different question")

            self.assertEqual(res[UDP].sport, req[UDP].dport, "Wrong response source port")
            self.assertEqual(res[UDP].dport, req[UDP].sport, "Wrong response destination port")

            self.assertEqual(res[IP].proto, 17, "Wrong response protocol")
            self.assertEqual(req[IP].src, self.src_ip, "Wrong request source ip")
            self.assertEqual(req[IP].dst, self.serv, "Wrong request destination ip")
            self.assertEqual(res[IP].src, req[IP].dst, "Wrong response source ip")
            self.assertEqual(res[IP].dst, req[IP].src, "Wrong response source ip")

if __name__ == '__main__':
    unittest.main()