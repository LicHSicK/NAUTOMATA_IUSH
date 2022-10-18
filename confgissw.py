import datetime
import netmiko
import os
from netmiko import ConnectHandler, NetmikoTimeoutException, NetMikoAuthenticationException
from sendemail import send_email


def createvlan():
    core1 = {
        'device_type': 'cisco_ios',
        'host': '10.255.255.1',
        'username': 'nautomata',
        'password': 'nautomata123',
        'secret': 'nautomata123'
    }
    core2 = {
        'device_type': 'cisco_ios',
        'host': '10.255.255.2',
        'username': 'nautomata',
        'password': 'nautomata123',
        'secret': 'nautomata123'
    }
    dist = {
        'device_type': 'cisco_ios',
        'host': '10.255.255.3',
        'username': 'nautomata',
        'password': 'nautomata123',
        'secret': 'nautomata123'
    }
    ctrl = 0
    while ctrl == 0:
        vlanid = str(input('Ingrese el vlan id a configurar\n'))
        name = str(input('Ingrese el nombre de la vlan a configurar\n'))
        ip1 = str(input('Ingrese la IP del core1\n'))
        ip2 = str(input('Ingrese la IP del core2\n'))
        netmask = str(input('Ingrese la mascara de subred\n'))
        verstb = str(input('Ingrese el ID del HSRP\n'))
        ipstb = str(input('Ingrese la IP de standby\n'))
        if ip1 == ip2 or ip1 == ipstb:
            print('Las ip no deben ser iguales')
        else:
            ctrl = 1
    try:
        command = ['vlan ' + vlanid, 'name ' + name, 'exit', 'interface vlan ' + vlanid, 'ip address ' + ip1 + ' ' +
                   netmask, 'standby version 2', 'standby ' + verstb + ' ip ' + ipstb, 'standby ' + verstb + ' ' +
                   'priority 120', 'standby ' + verstb + ' ' + ' preempt', 'standby ' + verstb + ' '
                   + ' authentication cisco123', 'no sh', 'interface ethernet0/0', 'switchport trunk allowed vlan add '
                   + vlanid]
        net_connect = ConnectHandler(**core1)
        net_connect.enable()
        output1 = net_connect.send_config_set(command, read_timeout=60, cmd_verify=False)
        net_connect.disconnect()
    except netmiko.exceptions.NetmikoTimeoutException:
        send_email('andres.ortizb@comunidad.iush.edu.co',
                   'Se presenta error de timeout sobre el dispositivo ' + core1['host'],
                   '\nIngenieros, se presenta error de timeout sobre el dispositivo ' + core1['host'] +
                   '. Por favor garantizar la conectividad contra el dispositivo', )
    except netmiko.exceptions.NetmikoAuthenticationException:
        send_email('andres.ortizb@comunidad.iush.edu.co',
                   'Se presenta error de credenciales sobre el dispositivo ' + core1['host'],
                   '\nIngenieros, se presenta error de credenciales sobre el dispositivo '
                   + core1['host'] +
                   '. Por favor garantiza que las credenciales para el usuario nautomata sean las correctas', )
    try:
        command1 = ['vlan ' + vlanid, 'name ' + name, 'exit', 'interface vlan ' + vlanid, 'ip address ' + ip2 + ' ' +
                    netmask, 'standby version 2', 'standby ' + verstb + ' ip ' + ipstb, 'standby ' + verstb + ' ' +
                    'priority 110', 'standby ' + verstb + ' ' + ' authentication cisco123', 'no sh',
                    'interface ethernet0/0', 'switchport trunk allowed vlan add ' + vlanid]
        net_connect = ConnectHandler(**core2)
        net_connect.enable()
        output2 = net_connect.send_config_set(command1, read_timeout=60, cmd_verify=False)
        net_connect.disconnect()
    except netmiko.exceptions.NetmikoTimeoutException:
        send_email('andres.ortizb@comunidad.iush.edu.co',
                   'Se presenta error de timeout sobre el dispositivo ' + core2['host'],
                   '\nIngenieros, se presenta error de timeout sobre el dispositivo ' + core2['host'] +
                   '. Por favor garantizar la conectividad contra el dispositivo', )
    except netmiko.exceptions.NetmikoAuthenticationException:
        send_email('andres.ortizb@comunidad.iush.edu.co',
                   'Se presenta error de credenciales sobre el dispositivo ' + core2['host'],
                   '\nIngenieros, se presenta error de credenciales sobre el dispositivo '
                   + core2['host'] +
                   '. Por favor garantiza que las credenciales para el usuario nautomata sean las correctas', )
    try:
        command3 = ['vlan ' + vlanid, 'name ' + name, 'exit', 'interface range ethernet 0/0 - 1',
                    'switchport trunk allowed vlan add ' + vlanid]
        net_connect = ConnectHandler(**dist)
        net_connect.enable()
        output2 = net_connect.send_config_set(command3, read_timeout=60, cmd_verify=False)
        net_connect.disconnect()
    except netmiko.exceptions.NetmikoTimeoutException:
        send_email('andres.ortizb@comunidad.iush.edu.co',
                   'Se presenta error de timeout sobre el dispositivo ' + dist['host'],
                   '\nIngenieros, se presenta error de timeout sobre el dispositivo ' + dist['host'] +
                   '. Por favor garantizar la conectividad contra el dispositivo', )
    except netmiko.exceptions.NetmikoAuthenticationException:
        send_email('andres.ortizb@comunidad.iush.edu.co',
                   'Se presenta error de credenciales sobre el dispositivo ' + dist['host'],
                   '\nIngenieros, se presenta error de credenciales sobre el dispositivo '
                   + dist['host'] +
                   '. Por favor garantiza que las credenciales para el usuario nautomata sean las correctas', )
