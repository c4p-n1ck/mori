__version__ = 0.1

from requests_html import HTMLSession, AsyncHTMLSession
from inspect import iscoroutinefunction
from fp.fp import FreeProxy
from time import time
from psutil import process_iter
from os import kill
from signal import SIGHUP
from stoyled import *
from .extra import *


print(info(f'Started mori v{__version__} -> {fetchFormatedTime()}'))
proxy = FreeProxy(rand=True).get(); local_tor_proxy = 'socks5://127.0.0.1:9050'
# local_tor_proxy = 'socks5://127.0.0.1:9050'; proxy = local_tor_proxy
print(good(f'Using "{proxy}" -> {fetchFormatedTime()}'))
c, ac = HTMLSession(), AsyncHTMLSession()
client, aclient = HTMLSession(), AsyncHTMLSession()
tclient, taclient = HTMLSession(), AsyncHTMLSession()
client.proxies = {
    'http': proxy,
    'https': proxy
}; aclient.proxies = {
    'http': proxy,
    'https': proxy
}; tor_proxies = {
    'http': local_tor_proxy,
    'https': local_tor_proxy
}; tclient.proxies = tor_proxies; taclient.proxies = tor_proxies


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
        client.proxies = {
        'http': proxy,
        'https': proxy
        }; aclient.proxies = {
        'http': proxy,
        'https': proxy
        }; print(good(f'Using "{proxy}" -> {fetchFormatedTime()}'))
    else:
        return change_proxy()
    if not check_proxy({'http': new_proxy, 'https': new_proxy}):
        return check_proxy()
    return proxy


def change_tor_ip():
    pid = 0
    for pinfo in process_iter():
        if pinfo.name() == 'tor':
            pid = pinfo.pid
    if pid:
        kill(pid, SIGHUP)
        print(good(f'Changed TOR IP on -> {fetchFormatedTime()}'))


def pori(func):

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


    except KeyboardInterrupt as e:
        print(info('Caught -> [SIGINT]'))

    return task


def tori(func):

    global tclient, taclient

    try:

        if iscoroutinefunction(func):

            async def task(*args, **kwargs):
                global aclient

                time_before_exec = time()
                returned = await func(c=taclient, *args, **kwargs)
                time_after_exec = time()

                exec_time = time_after_exec - time_before_exec

                print(info(f"{func.__name__} took -> {exec_time:.2f}µ"))
                return returned
        else:

            def task(*args, **kwargs):
                global client

                time_before_exec = time()
                returned = func(c=tclient, *args, **kwargs)
                time_after_exec = time()

                exec_time = time_after_exec - time_before_exec

                print(info(f"{func.__name__} took -> {exec_time:.2f}µ"))
                return returned

    except Exception as e:
        print(bad(f'Error -> {e}'))

    except KeyboardInterrupt as e:
        print(info('Caught -> [SIGINT]'))

    return task


def check_proxy(proxies, url='https://google.com'):
    """
    Check if a proxy is working, basically tries a GET request to the URL with the proxy
        Parameters:
            proxies (dict): Dictionary consisting of proxies
            url (str): URL to to check with proxy

        Returns:
            bool: Boolean, if proxy is working or not
    """
    try:
        c.head(
                url,
                proxies=proxies,
                headers={
                            'User-Agent': f'mori/{__version__}'
                        }
            )
    except Exception as err:
        print(bad(f'ERROR -> {err}'))
        return False
    return True
