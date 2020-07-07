#!/usr/bin/python

# This file is part of Sampler.
# 
# Sampler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# Sampler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


import liblo, sys

import pickle

from time import sleep

import subprocess


class Server:

    # send all messages to port 26903 on the local machine
    try:
        puredata = liblo.Address(26903)
    except liblo.AddressError, err:
        print str(err)
        sys.exit()

    # And create server
    try:
        server = liblo.Server(26904)
    except liblo.ServerError, err:
        print str(err)
        sys.exit()


    # Data Table
    data = []

    # Fichier de config :
    filepath = 'config.conf'


    def add_data(self, path, args):
        print("Add '" + args[0] + "' to Data[]")
        print(self.data)
        self.data.append(args[0])

    def init_data(self, path, args):
        self.data = ['null']*args[0]
        print("Data initialized to " + str(args[0]) + " cells.")
        
    def write_data(self, path, args):
        with open(self.filepath, 'wb') as fp:
           pickle.dump(self.data, fp)
        
        print ("Data writed.")
        #self.data = []

    def read_data(self, path, args):
        print("Clear and Read data... :")
        self.data = []
        
        with open (self.filepath, 'rb') as fp:
            self.data = pickle.load(fp)
            
        print(self.data)

    def get_data(self, path, args):
        # Clear List for update
        print("Begin of sending Data..")
        msg = liblo.Message("/data/clear")
        liblo.send(self.puredata, msg)
        
        for i in range(0, len(self.data)):
#            print(self.data[i])
            if self.data[i] != 'null' :
              liblo.send(self.puredata, "/data/add", ('i', i), ('s', self.data[i]))
#            sleep(0.01)
            
        msg = liblo.Message("/data/update")
        liblo.send(self.puredata, msg)
        
        print ("Data sended")
    
    def get_data_item(self, path, args):
        print("Get Data[" + str(args[0]) + "] : '" + self.data[args[0]] + "'.")
        
        liblo.send(self.puredata, "/data/set", ('i', args[0]), ('s', self.data[args[0]]))
        
    def set_data_item(self, path, args):
        print("Set Data[" + str(args[0]) + "] : '" + args[1] + "'.")
        
        self.data[args[0]]=args[1]
    
    def default_callback(self, path, args):
        print("No operation with '" + path + "'.")
        
    def get_data_length(self, path, args):
        print("Get Data Lendth : " + str(len(self.data)) + ".")
        liblo.send(self.puredata, "/data/length", ('i', len(self.data)))
    
    def __init__(self):
        self.server.add_method("/data/add", 's', self.add_data)
        self.server.add_method("/data/init", 'i', self.init_data)
        self.server.add_method("/data/write", None, self.write_data)
        self.server.add_method("/data/read", None, self.read_data)
        self.server.add_method("/data/get", None, self.get_data)
        self.server.add_method("/data/get_item", 'i', self.get_data_item)
        self.server.add_method("/data/set_item", 'is', self.set_data_item)
        self.server.add_method("/data/length", None, self.get_data_length)
        self.server.add_method(None, None, self.default_callback)

        print("#######################################################################")
        print("###########               Sampler Initialized              ############")
        print("#######################################################################")
        while True:
            self.server.recv(100)


#pdProcess = subprocess.call(['pd', '-rt', '-jack', '-inchannels', '0', '-outchannels', '32', '-alsamidi', '-midiindev', '1', '-open', './BnB_Sampler.pd', '-send', '"; pd dsp 1"'], stderr=subprocess.STDOUT)
#subprocess.call(['ls', '-l'])

server = Server()
