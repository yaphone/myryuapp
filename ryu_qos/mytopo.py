from mininet.topo import Topo
class MininetTopo(Topo):
    def __init__(self,**opts):
        Topo.__init__(self, **opts)
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost('h4')
        host5 = self.addHost('h5')
        host6 = self.addHost('h6')
        host7 = self.addHost('h7')
        host8 = self.addHost('h8')
        host9 = self.addHost('h9')
        host10 = self.addHost('h10')
    
        self.switch = {}
        for s in range(1,6):
            self.switch[s-1] = self.addSwitch('s%s' %(s))
        self.addLink(self.switch[0], self.switch[1])
        self.addLink(self.switch[0], self.switch[2])
        self.addLink(self.switch[0], self.switch[3])
        self.addLink(self.switch[4], self.switch[1])
        self.addLink(self.switch[4], self.switch[2])
        self.addLink(self.switch[4], self.switch[3])
            #Adding host
        self.addLink(self.switch[0], host1)
        self.addLink(self.switch[4], host2)
        self.addLink(self.switch[4], host3)
        self.addLink(self.switch[4], host4)
        self.addLink(self.switch[4], host5)
        self.addLink(self.switch[4], host6)
        self.addLink(self.switch[4], host7)
        self.addLink(self.switch[4], host8)
        self.addLink(self.switch[4], host9)
        self.addLink(self.switch[4], host10)
        
topos = {'group':(lambda:MininetTopo())}