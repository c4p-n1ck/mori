#!/usr/bin/env python3


from time import sleep
from mori import pori, change_proxy, run, tori, change_tor_ip, c, ac


@pori
def check(c):
    resp = c.get('https://httpbin.org/ip')
    print(resp.json())

@pori
async def acheck(c):
    resp = await c.get('https://httpbin.org/ip')
    print(resp.json())
    resp = await c.get('https://httpbin.org/ip')
    print(resp.json())


@tori
async def tacheck(c):
    resp = await c.get('https://httpbin.org/ip')
    print(resp.json())
    change_tor_ip()
    sleep(.84)
    resp = await c.get('https://httpbin.org/ip')
    print(resp.json())

@tori
def tcheck(c):
    resp = c.get('https://httpbin.org/ip')
    print(resp.json())


def ncheck():
    resp = c.get('https://httpbin.org/ip')
    print(resp.json())


async def nacheck():
    resp = await ac.get('https://httpbin.org/ip')
    print(resp.json())


run(tacheck)
change_tor_ip()
tcheck()
run(acheck)
change_proxy()
check()
run(nacheck)
ncheck()
