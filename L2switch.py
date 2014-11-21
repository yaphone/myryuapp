from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class L2Switch(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
	
	def __init__(self, *args, **kwargs):
		super(L2Switch, self).__init__(*args, **kwargs)
		self.mac_to_port = {}
		
	def add_flow(self, datapath, priority, match, actions):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		
		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
		mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
		datapath.send_msg(mod)
	
	
	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def packet_in_handler(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		in_port = msg.match['in_port']
		
		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]
		
		dst = eth.dst
		src = eth.src
		
		dpid = datapath.id
		self.mac_to_port.setdefault(dpid, {})
		
		self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
		
		# learn a mac address to avoid FLOOD next time
		self.mac_to_port[dpid][src] = in_port
		
		if dst in self.mac_to_port[dpid]:
			out_port = self.mac_to_port[dpid][dst]
		else:
			out_port = ofproto.OFPP_FLOOD
			
		actions = [parser.OFPActionOutput(out_port)]
			
		# install a flow to avoid a packet_in next time
		
		if out_port!= ofproto.OFPP_FLOOD:
			match = parser.OFPMatch(in_port, eth_dst=dst)
			self.add_flow(datapath, 1, match, actions)
			
		data = None
		if msg.buffer_id == ofproto.OFP_NO_BUFFER:
			data = msg.data
		
		out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)
		
		datapath.send_msg(out)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		