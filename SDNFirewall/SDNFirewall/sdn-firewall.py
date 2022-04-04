#!/usr/bin/python
# CS 6250 Spring 2022 - SDN Firewall Project with POX
# build purple-05

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.revent import *
from pox.lib.addresses import IPAddr, EthAddr

# You may use this space before the firewall_policy_processing function to add any extra function that you 
# may need to complete your firewall implementation.  No additional functions "should" be required to complete
# this assignment.


def firewall_policy_processing(policies):
	
	rules = []
	
	for policy in policies:
		# Enter your code here to implement matching and block/allow rules.  See the links
		# in Implementation Hints on how to do this. 
		# HINT:  Think about how to use the priority in your flow modification.

		# rule = None # Please note that you need to redefine this variable below to create a valid POX Flow Modification Object
		rule = of.ofp_flow_mod()
		# always going to be IPv4
		rule.match.dl_type = 0x0800
		
		if(policy["mac-src"] != "-"):
			rule.match.dl_src = EthAddr(policy["mac-src"])
		
		if(policy["mac-dst"] != "-"):
			rule.match.dl_dst = EthAddr(policy["mac-dst"])
		
		if(policy["ip-src"] != "-"):
			rule.match.nw_src = (policy["ip-src"])
		
		if(policy["ip-dst"] != "-"):
			rule.match.nw_dst = (policy["ip-dst"])
			
		if(policy["ipprotocol"] != "-"):
			rule.match.nw_proto = int(policy["ipprotocol"])
			if(policy["ipprotocol"] == "6" or policy["ipprotocol"] == "17"):
				if(policy["port-src"] != "-"):
					rule.match.tp_src = int(policy["port-src"])
				if(policy["port-dst"] != "-"):
					rule.match.tp_dst = int(policy["port-dst"])
		
		if(policy["action"] == "Allow"):
			rule.priority = 32767
			rule.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
		
		if(policy["action"] == "Block"):
			rule.priority = 1
			#rule.actions.append(of.ofp_action_outport(port = OFPP_NONE))

		# End Code Here
		print('Added Rule ',policy['rulenum'],': ',policy['comment'])
		#print(rule)   #Uncomment this to debug your "rule"
		rules.append(rule)

	return rules
