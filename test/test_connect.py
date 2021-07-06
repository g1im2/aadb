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

if __name__ == '__main__':
    aadb.start(main())
