# -*- coding: utf-8 -*-
__author__ = 'murre'

from direct.showbase.ShowBase import ShowBase
from twisted.internet.task import LoopingCall
from twisted.internet import reactor, defer
from twisted.internet.threads import deferToThread
from twisted.internet.protocol import Protocol, Factory, ClientFactory
from direct.actor.Actor import Actor

from utility.enum import *
import json
import sys

isServer = "-s" in sys.argv
print sys.argv
if isServer:
    print 'Mode: server'
else:
    print 'Mode: client'

