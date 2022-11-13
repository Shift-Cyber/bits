#!/usr/bin/bash

# open the ssh tunnel to expose mysql to the worker
$(while true; do sshpass -p$SSH_PASSWD ssh -o "StrictHostKeyChecking=no" -4 -N -L 3336:127.0.0.1:3306 $SSH_USER@$SSH_HOST; done) &

# give it a few seconds to connect the tunnel
sleep 5

# start the worker
python3 worker.py
