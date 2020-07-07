#!/bin/sh

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

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
    

a2jmidid -e &

(sleep 1 && pd -rt -jack -inchannels 0 -outchannels 32 -alsamidi -midiindev 1 -open ./BnB_Sampler.pd -send "; pd dsp 1") >> pd.log &
python SaveScript.py
