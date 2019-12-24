#!/bin/bash

#class_puzzle_contact_algo.py
#class_puzzle_contact_and.py
#controller_communications.py
#ms_puzzle_ctrl_reactor.py
#ms_puzzle_ctrl_multi.py

USERNAME="pi"
PASSWORD="raspberry"

echo "Deploying the multi puzzle controller.."
sshpass -p${PASSWORD} scp class_puzzle_contact_and.py controller_communications.py ms_puzzle_ctrl_multi.py ${USERNAME}@192.168.1.31:/opt/questfactor/puzzle

echo "Deploying to the reactor puzzle controller.."
sshpass -p${PASSWORD} scp class_puzzle_contact_algo.py controller_communications.py ms_puzzle_ctrl_reactor.py ${USERNAME}@192.168.1.30:/opt/questfactor/puzzle

echo "Deploying to the media controller (countdown TVs)"
sshpass -p${PASSWORD} scp start-chromium.sh media.service media_communications.py ${USERNAME}@192.168.1.111:/opt/questfactor/media
