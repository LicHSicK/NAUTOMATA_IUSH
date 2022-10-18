import datetime
import netmiko
import os
from sendemail import send_email
from netmiko import ConnectHandler, NetmikoTimeoutException, NetMikoAuthenticationException

today = datetime.datetime.today()
todaystring = today.strftime("%Y-%m-%d")

def backupCisco():
    devices = '/home/nautomata/NAUTOMATA_IUSH/devices.txt'
    with open(devices) as CI:
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
                output1 = net_connect.send_command('show running')
                net_connect.disconnect()
                newpath = '/home/nautomata/NAUTOMATA_IUSH/BackUPCI/' + output
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                filebk = open('/home/nautomata/NAUTOMATA_IUSH/BackUPCI/' + output + '/' + network_devices['host']
                              + '_Backup_' + todaystring + '.txt', 'w+')
                filebk.write(output1)
                filebk.close()
                send_email('andres.ortizb@comunidad.iush.edu.co',
                           'BackUP realizado de manera satisfactoria al dispositivo ' + output,
                           '\nIngenieros, se realiza de manera sarisfactoria el BK del dispositivo ' + output +
                           ' Se guardará una copia en el repositorio /home/nautomata/NAUTOMATA_IUSH/BackUPCI/',
                           '/home/nautomata/NAUTOMATA_IUSH/BackUPCI/' + output + '/' + network_devices['host']
                           + '_Backup_' + todaystring + '.txt')
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


