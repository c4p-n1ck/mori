#!/usr/bin/env python3


from mori import gori, change_proxy, run, dore


@gori
def check(c):
    resp = c.get('https://httpbin.org/ip')
    print(resp.json())


@gori
async def acheck(c):
    resp = await c.get('https://httpbin.org/ip')
    print(resp.json())
    resp = await c.get('https://httpbin.org/ip')
    print(resp.json())


run(acheck)
change_proxy()
check()
