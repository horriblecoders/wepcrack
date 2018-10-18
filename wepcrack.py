#wepcrack.py
import subprocess
import os

def find_wireless_cards():
	iwconfig_output = subprocess.check_output('iwconfig').decode('utf-8')
	num_cards = iwconfig_output.count('wlan')
	if iwconfig_output.count('mon0'):
		return ["mon0"]
	wireless_names = []
	last_found = 0
	for x in range(num_cards):
		last_found = iwconfig_output.find('wlan',last_found)
		wireless_names.append(iwconfig_output[last_found:iwconfig_output.find(' ',last_found)])
		last_found += 1
	return wireless_names

def enable_monitor_mode(wireless_cards): #Should be modified slightly to be sure network card is set as mon0 and not mon1 etc...
	if 'mon0' in wireless_cards:
		print("Already in monitor mode!")
		return 'mon0'
	for card in wireless_cards:
		command = 'sudo airmon-ng start '+str(card)
		command = command.split(' ')
		output = subprocess.call(command)
		if "mon0" in subprocess.check_output('iwconfig').decode('utf-8'):
			print("Chip set in monitor mode")
			return 'mon0'
	return None

def find_bssid(mon_mode_card):
	if 'mon' not in mon_mode_card:
		print("Problem using monitor mode enabled card. Does the network card support monitor mode?")
	command = 'sudo airodump-ng mon0'
	output = subprocess.call(command.split())
	print(output)

print("PROGRAM MUST BE RUN AS SUPER USER!")
#Include a check if the program was run as root
wireless_cards = find_wireless_cards()
mon_mode_card = enable_monitor_mode(wireless_cards)
test_output = find_bssid(mon_mode_card)
