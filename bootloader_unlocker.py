# **This script is not mine, I just modified it to work with the new bootloader unlock method.**

import signal
import sys
import os
import subprocess
import math
import time

def reboot_to_fastboot():
    os.system("adb reboot bootloader")
    time.sleep(5)

def check_fastboot_mode():
    result = os.popen("fastboot devices").read()
    if "fastboot" in result:
        print("Device is in Fastboot mode. Continuing...")
    else:
        print("Device is not in Fastboot mode. Rebooting the device to Fastboot mode...")
        reboot_to_fastboot()
        result = os.popen("fastboot devices").read()
        if "fastboot" in result:
            print("Device is now in Fastboot mode. Continuing...")
        else:
            print("Failed to reboot to Fastboot mode. Exiting.")
            sys.exit(1)

def verify_imei(imei):
    imei_translation = str.maketrans({'-': '', ' ': ''})
    translated_imei = imei.translate(imei_translation)

    sum_digits = 0
    for i, digit in enumerate(translated_imei):
        digit_value = int(digit)
        if i % 2 == 0:
            sum_digits += digit_value
        else:
            doubled_digit = digit_value * 2
            sum_digits += doubled_digit // 10 + doubled_digit % 10

    return sum_digits % 10 == 0

def handle_error(result, base_start):
    if "Command not allowed" in result:
        print(f"Error: Command not allowed for IMEI {base_start}.")
        print("This may be due to restrictions on your device.")
        print("Please check device settings and consult manufacturer documentation.")
        sys.exit(1)
    else:
        print(f"Unknown error for IMEI {base_start}.")
        sys.exit(1)

def resumer(signum, frame):
    print("\n\nLast used code was:", base_start)
    with open("lastcode", "w") as fp:
        fp.write(str(base_start))
    sys.exit(1)

def bruteforceBootloader(increment):
    algoOEMcode = 1000000000000000  # base to start bruteforce from
    autoreboot = False  # set this to True if you need to prevent the automatic reboot to system by the bootloader
    autorebootcount = 4  # reboot every x attempts if autoreboot is True, set this one below the automatic reboot by the bootloader
    savecount = 200  # save progress every 200 attempts, do not set too low to prevent storage wearout
    unknownfail = True  # fail if output is unknown, only switch to False if you have problems with this

    failmsg = "check password failed"  # used to check if code is wrong

    unlock = False
    n = 0
    while not unlock:
        print("Bruteforce is running...\nCurrently testing code "+str(algoOEMcode).zfill(16)+"\nProgress: "+str(round((algoOEMcode/10000000000000000)*100, 2))+"%")
        
        command = ["fastboot", "oem", "unlock", str(algoOEMcode).zfill(16)]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(result.stderr)
        n += 1

        if 'success' in result.stderr.lower():
            print("Bootloader unlocked successfully! OEM CODE: " + str(algoOEMcode))
            os.system("fastboot oem unlock " + str(algoOEMcode).zfill(16))
            return algoOEMcode
        if 'reboot' in result.stderr.lower():
            print("Target device has bruteforce protection!")
            print("Waiting for reboot and trying again...")
            os.system("adb wait-for-device")
            os.system("adb reboot bootloader")
            print("Device reboot requested, turning on reboot workaround.")
            autoreboot = True
        if failmsg in result.stderr.lower():
            # print("Code " + str(algoOEMcode) + " is wrong, trying next one...")
            pass
        if 'success' not in result.stderr.lower() and 'reboot' not in result.stderr.lower() and failmsg not in result.stderr.lower() and unknownfail:
            # fail here to prevent continuing bruteforce on success or another error the script cant handle
            print("Could not parse output.")
            print("Please check the output above yourself.")
            print("If you want to disable this feature, switch variable unknownfail to False")
            exit()

        if n % savecount == 0:
            bak = open("unlock_code.txt", "w")
            bak.write("If you need to pick up where you left off,\nchange the algoOEMcode variable with #base comment to the following value :\n"+str(algoOEMcode))
            bak.close()
            print("Your bruteforce progress has been saved in \"unlock_code.txt\"")

        if n % autorebootcount == 0 and autoreboot:
            print("Rebooting to prevent bootloader from rebooting...")
            os.system('fastboot reboot bootloader')

        algoOEMcode += increment

        if algoOEMcode > 10000000000000000:
            print("OEM Code not found!\n")
            os.system("fastboot reboot")
            exit()

def luhn_checksum(imei):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(imei)
    oddDigits = digits[-1::-2]
    evenDigits = digits[-2::-2]
    checksum = 0
    checksum += sum(oddDigits)
    for i in evenDigits:
        checksum += sum(digits_of(i*2))
    return checksum % 10

def main():
    global base_start
    signal.signal(signal.SIGINT, resumer)
    signal.signal(signal.SIGTERM, resumer)

    check_fastboot_mode()
    # Insert the IMEI here to start from a specific point in the bruteforce process
    imei = input("Enter IMEI: ")

    if not verify_imei(imei):
        print("Invalid IMEI! Exiting.")
        sys.exit(1)

    base_start = int(imei)

    fou = "fastboot oem unlock "

    while True:
        TOTAL = f"{fou}{base_start}"
        result = os.popen(TOTAL).read()

        if "OKAY" in result or "finished" in result:
            base_start += 1
        else:
            handle_error(result, base_start)

if __name__ == "__main__":
    main()