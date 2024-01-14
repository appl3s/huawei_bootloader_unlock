# Bootloader Unlock Script

This Python script is designed to unlock the bootloader of an Android device through a brute force method. The script uses Fastboot commands to attempt unlocking the bootloader with different codes until successful. Note that brute-forcing a bootloader is not always ethical or legal, and it may void your device's warranty or violate terms of service.

## Prerequisites
- [Fastboot](https://developer.android.com/studio/releases/platform-tools) installed on your computer.
- [ADB](https://developer.android.com/studio/releases/platform-tools) installed on your computer.
- Python 3 installed.

## Usage

1. Connect your Android device to your computer via USB.
2. Make sure your device is in Fastboot mode.
3. Run the script using the following command:

    ```bash
    python3 bootloader_unlocker.py
    ```

4. Enter the IMEI when prompted.
5. The script will attempt to unlock the bootloader using a brute force method.

## Important Notes

- The script attempts to unlock the bootloader by incrementing a base code. It may take a considerable amount of time.
- Use this script responsibly and make sure you have the legal right to unlock the bootloader.
- Unlocking the bootloader may void your device's warranty and could lead to data loss.
- Some devices may have protections against brute-force attacks, and this script might not work for all devices.

## Troubleshooting

If you encounter any issues, consider the following:

- Ensure that Fastboot and ADB are properly set up on your computer.
- Make sure your device is connected, and the Fastboot mode is accessible.
- Verify that your device allows bootloader unlocking.

**Disclaimer:** Use this script at your own risk. The provided information and script are for educational purposes only. The author and publisher are not responsible for any misuse or damage caused by this script.