# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *
from StpSwitch import *


# msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough) 



class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.rootNode = idNum
        self.distanceToRoot = 0
        self.activeLinks = set()
        self.neighborHop = idNum


    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        
        claimedRoot = self.switchID
        distanceToRoot = 0
        originID = self.switchID
        pathThrough = False

        for neighbor in self.links:
            destinationID = neighbor
            msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough)
            self.send_message(msg)
        return

        
    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        claimedRoot = message.root
        distanceToRoot = message.distance
        originID = message.origin
        destinationID = message.destination
        pathThrough = message.pathThrough

        if claimedRoot < self.rootNode:
            self.rootNode = claimedRoot
            self.distanceToRoot = distanceToRoot+1
            self.activeLinks.add(originID)
            self.neighborHop = originID
            for neighbor in self.links:
                msg = Message(self.rootNode, self.distanceToRoot, self.switchID, neighbor, False)
                if self.neighborHop == neighbor:
                    msg.pathThrough = True
                self.send_message(msg)


        # claimedroot > self.rootnode
        # claimedroot == self.root
        elif claimedRoot == self.rootNode and distanceToRoot+1 < self.distanceToRoot:
            self.distanceToRoot = distanceToRoot+1
            self.activeLinks.remove(neighborHop)
            self.neighborHop = originID
            self.activeLinks.add(originID)
            for neighbor in self.links:
                msg = Message(self.root, self.distanceToRoot, self.switchID, neighbor, False)
                if self.neighborHop == neighbor:
                    msg.pathThrough = True
                self.send_message(msg)

        elif claimedRoot == self.rootNode and distanceToRoot+1 == self.distanceToRoot and originID < self.neighborHop:
            self.activeLinks.remove(self.neighborHop)
            self.neighborHop = originID
            self.activeLinks.add(originID)
            for neighbor in self.links:
                msg = Message(self.rootNode, self.distanceToRoot, self.switchID, neighbor, False)
                if self.neighborHop == neighbor:
                    msg.pathThrough = True
                self.send_message(msg)


        if pathThrough and originID not in self.activeLinks:
            self.activeLinks.add(originID)

        if not pathThrough and originID in self.activeLinks and self.neighborHop != message.origin:
            self.activeLinks.remove(originID)

        return

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        output = ""
        for link in sorted(self.activeLinks):
            output += str(self.switchID) + " - " + str(link) + ", "
        
        return output[:-2]

