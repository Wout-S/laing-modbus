# laing-modbus
Simple python gui to control Laing desk motor controllers via Modbus. Documentation can be found in [/Resources](/Resources/)

## Hardware

The RJ12 connector on the LTC series has the following pinout:
1. +5V Output
2. RS485 A
3. RS485 B
4. +5V Input
5. Analog control panel
6. Ground
<br>
![Pinout](/images/RJ12_pinout.png)

### Analog control
Up/Down can be controlled by changing the resistance between pin 5 and 6. The following resistances should be applied:
- Idle: 22k $\Omega$
- UP: 11k $\Omega$
- Down: 3.3k $\Omega$
