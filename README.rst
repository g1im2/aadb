Aadb
=====
It is a lightweight Python version of Android debug bridge, it is built according to the Google ADB transport protocol, fully asynchronous call mode is its feature. Of course, using asynchronous calls allows you to execute multiple commands at the same time, which makes it much easier to control your Android device.

It uses Asyncio to build asynchronous communications and is fully compatible with and supports Asyncio, that is, it can only support Python 3.

Installing
--------------
Install and update using `pip`_:

.. code-block:: text

    $ pip install -U aadb

.. _pip: https://pip.pypa.io/en/stable/quickstart/

A Simple Example
---------------
.. code-block:: python

    import aadb
    import asyncio


    async def main():
        adb = aadb.create_bridge()
        device = (await adb.devices())[0]
        asyncio.create_task(device.logcat(pipeline=lambda x: print(x)))
        await asyncio.sleep(3)
        print(await device.get_properties())
        await asyncio.sleep(3)
        print(await device.list_package())
        await device.shell('dumpsys meminfo', pipeline=lambda x: print(x))

.. code-block:: python

    if __name__ == '__main__':
    aadb.start(main())
