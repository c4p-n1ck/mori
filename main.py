#!/usr/bin/env python3


from mori import pori, change_proxy, run, tori, change_tor_ip


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
    resp = await c.get('https://httpbin.org/ip')
    print(resp.json())

@tori
def tcheck(c):
    resp = c.get('https://httpbin.org/ip')
    print(resp.json())


run(tacheck)
tcheck()
run(acheck)
change_proxy()
check()
