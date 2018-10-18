#wepcrack.py
import subprocess
import os

def find_wireless_cards():
	iwconfig_output = subprocess.check_output('iwconfig')
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

def enable_monitor_mode(wireless_cards):
	if 'mon0' in wireless_cards:
		print("Already in monitor mode!")
		return 'mon0'
	for card in wireless_cards:
		command = 'sudo airmon-ng start '+str(card)
		command = command.split(' ')
		output = subprocess.call(command)
		if "mon0" in subprocess.check_output('iwconfig'):
			print("Chip set in monitor mode")
			return 'mon0'
	return None

print("You will be prompted to enter your password at least once")

wireless_cards = find_wireless_cards()
mon_mode_card = enable_monitor_mode(wireless_cards)

