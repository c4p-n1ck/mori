from requests_html import HTMLSession, AsyncHTMLSession
from inspect import iscoroutinefunction
from fp.fp import FreeProxy
from time import time
from stoyled import *


print(info(f'Started -> {fetchFormatedTime()}'))
proxy = FreeProxy(rand=True).get()
print(good(f'Using "{proxy}" -> {fetchFormatedTime()}'))
client, aclient = HTMLSession(), AsyncHTMLSession()
client.proxies = {
    'http': proxy,
    'https': proxy
}; aclient.proxies = {
    'http': proxy,
    'https': proxy
};


def run(*args, **kwargs):
    try:
        return aclient.run(*args, **kwargs)
    except Exception as e:
        print(bad(f'Exception -> {e}'))


def change_proxy():
    global proxy, client, aclient
    new_proxy = FreeProxy(country_id=['US', 'BR'], timeout=0.4, rand=True).get()
    if new_proxy != proxy:
        proxy = new_proxy
    else:
        return change_proxy()
    client.proxies = {
    'http': proxy,
    'https': proxy
    }; aclient.proxies = {
    'http': proxy,
    'https': proxy
    }; print(good(f'Using "{proxy}" -> {fetchFormatedTime()}'))
    return proxy


def gori(func):

    global client, aclient

    try:

        if iscoroutinefunction(func):

            async def task(*args, **kwargs):
                global aclient

                time_before_exec = time()
                returned = await func(c=aclient, *args, **kwargs)
                time_after_exec = time()

                exec_time = time_after_exec - time_before_exec

                print(info(f"{func.__name__} took -> {exec_time:.2f}µ"))
                return returned
        else:

            def task(*args, **kwargs):
                global client

                time_before_exec = time()
                returned = func(c=client, *args, **kwargs)
                time_after_exec = time()

                exec_time = time_after_exec - time_before_exec

                print(info(f"{func.__name__} took -> {exec_time:.2f}µ"))
                return returned

    except Exception as e:
        print(bad(f'Error -> {e}'))


    return task
