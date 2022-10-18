import datetime
import netmiko
import os
from netmiko import ConnectHandler, NetmikoTimeoutException, NetMikoAuthenticationException
from sendemail import send_email

today = datetime.datetime.today()
todaystring = today.strftime("%Y-%m-%d")

def bwCisco():
    devices = '/home/nautomata/NAUTOMATA_IUSH/devices.txt'
    with open (devices) as CI:
        for IP in CI:
            network_devices = {
                'device_type': 'cisco_ios',
                'host': IP.strip(),
                'username': 'nautomata',
                'password': 'nautomata123',
                'secret': 'nautomata123'
            }
            try:
                net_connect = ConnectHandler(**network_devices)
                net_connect.enable()
                output = net_connect.find_prompt()
                output1 = net_connect.send_command('show interface ethernet 0/1 | i  minute.input.rate')
                net_connect.disconnect()
                output1 = output1.split()
                output1 = int(output1[4])
                if output1 > 8000000:
                    send_email('andres.ortizb@comunidad.iush.edu.co',
                               'Interfaz saturada en el dispositivo ' + output,
                               '\nIngenieros, se presenta saturación en la interfaz ethernet 0/1, por favor validar.'
                               )
                else:
                    print('La interfaz no presenta saturación')
            except netmiko.exceptions.NetmikoTimeoutException:
                send_email('andres.ortizb@comunidad.iush.edu.co',
                           'Se presenta error de timeout sobre el dispositivo ' + network_devices['host'],
                           '\nIngenieros, se presenta error de timeout sobre el dispositivo ' + network_devices['host'] +
                           '. Por favor garantizar la conectividad contra el dispositivo',)
            except netmiko.exceptions.NetmikoAuthenticationException:
                send_email('andres.ortizb@comunidad.iush.edu.co',
                           'Se presenta error de credenciales sobre el dispositivo ' + network_devices['host'],
                           '\nIngenieros, se presenta error de credenciales sobre el dispositivo '
                           + network_devices['host'] +
                           '. Por favor garantiza que las credenciales para el usuario nautomata sean las correctas',)


