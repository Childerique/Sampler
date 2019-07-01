#!/bin/sh

(sleep 1 && pd -rt -jack -inchannels 0 -outchannels 32 -alsamidi -midiindev 1 -open ./BnB_Sampler.pd -send "; pd dsp 1") >> pd.log &
python SaveScript.py
