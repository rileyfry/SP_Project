import asyncio
from bleak import BleakClient, BleakScanner

async def main():
    # Define the Bluetooth address of the HRM-Dual
    address = "F3:7C:B0:DD:7C:D0"  # Update this with your HRM-Dual Bluetooth address

    print(f"🔍 Scanning for HRM-Dual...")

    # Discover nearby Bluetooth devices for a longer period
    devices = await BleakScanner.discover(timeout=20)  # Increased timeout for scanning

    # Check if the HRM-Dual was found
    found_device = None
    for device in devices:
        if device.address == address:
            found_device = device
            print(f"✅ Found HRM-Dual at {device.address}")
            break

    if not found_device:
        print("❌ HRM-Dual not found!")
        return

    print("Connecting...")
    try:
        # Connecting with a longer timeout and detailed logging
        client = BleakClient(address, timeout=60.0)  # Increased timeout for connection
        print("Before connection attempt...")
        await client.connect()
        print("After connection attempt...")

        connected = await client.is_connected()

        if connected:
            print("✅ Connected successfully!")

            # Discover services after connecting
            print("Subscribing to heart rate notifications...")

            # Try to get the heart rate characteristic (make sure HRM-Dual is in motion)
            # The UUID is for heart rate monitoring
            heart_rate_uuid = "00002a37-0000-1000-8000-00805f9b34fb"

            # Subscribe to heart rate notifications
            await client.start_notify(heart_rate_uuid, notification_handler)

            # Wait for heart rate data (keep the script running)
            print("Receiving data... (Ctrl+C to stop)")
            await asyncio.Event().wait()

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
    finally:
        if client.is_connected:
            await client.disconnect()
            print("Disconnected.")

# Heart rate notification handler (prints received heart rate)
def notification_handler(data):
    heart_rate = int(data[1])  # Typically, heart rate data is in the second byte
    print(f"Heart rate: {heart_rate} BPM")

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
