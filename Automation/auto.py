#!/usr/bin/python3

from pwn import *

#io = process(["nmap", "127.0.0.1"])
#output = io.recvall()
#print(output.decode())

#io = process(["msfconsole", "-q"], stdin=PTY)
#io.recvuntil(b">") # Since msfconsole takes time and last it gives is >
#io.sendline(b"use exploit/multi/handler")
#io.sendline(b"set payload windows/x64/meterpreter/reverse_tcp")
#io.sendline(b"set lport 4444")
#io.sendline(b"set lhost enp7s0")

# Now we dont want python we just want to interact with msfconsole

#io.interactive()

# SSH
s1 = ssh(host="127.0.0.1",user="at0m",password="at0m")
#p1 = s1.shell("zsh")
#p1.interactive()
p2 = s1.process(["nmap","127.0.0.1"])
out = p2.recvall()
print(out.decode())
