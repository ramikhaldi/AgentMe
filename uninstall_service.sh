sudo systemctl stop agentme
sudo systemctl disable agentme
sudo rm /etc/systemd/system/agentme.service
sudo systemctl daemon-reload
