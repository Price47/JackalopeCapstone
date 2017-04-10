import socket

class Alarm:
	tcp_port = 55555
	tcp_address = "192.168.0.2"
	msg_alarm = "alarm"
	msg_off = "off"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self):
		s.connect((tcp_address, tcp_port))

	def alarm_on():
		s.send(msg_alarm)

	def alarm_off():
		s.send(msg_off)

	def __del__(self):
		s.close()