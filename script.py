import subprocess
import usb.core
import usb.backend.libusb1

def load_usb(print_all,VID,PID):
    backend = usb.backend.libusb1.get_backend(
        find_library=lambda x: "C://Users//LanaBeck//Software//libusb-1.0.27//VS2022//MS64//dll//libusb-1.0.dll")
    if backend is None:
        print("libusb not found!")
    else:
        print("libusb found and loaded!")

    usb_devices = usb.core.find(backend=backend, find_all=True)

    if print_all:
        for i, d in enumerate(usb_devices):
            print(i,d)

    dev = usb.core.find(idVendor=VID, idProduct=PID)
    if dev is None:
        raise ValueError('Device not found')
    if dev is None:
        print("Device not found")
    else:
        print("Device found:", dev)
    # dev.reset()

def compile_eclipse_project(eclipse_exe,project_path):
    command = [eclipse_exe, "-nosplash", "-application", "org.eclipse.cdt.managedbuilder.core.headlessbuild", "-build", project_path,"-configuration","debug"]
    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode == 0:
        print("Build successful.")
    else:
        print("Build failed.")
        print(process.stderr)

def load_FX3_image(cypress_fw_prog,fw_path):
    # # Run command with all arguments
    result = subprocess.run([
        cypress_fw_prog,
        "-fw", fw_path,
        "-dest", "SYSTEM",
        "-v"
    ], capture_output=True, text=True)
    # # Print the output and any errors
    print(result.stdout)
    print(result.stderr)

def load_USB_host(host_path):
    # # Run command with all arguments
    subprocess.run(f'start cmd /k "{host_path}"', shell=True)

def rebuild_host(VS_dev_env_path, host_sln_path,rebuild):
    if rebuild:
        subprocess.run([VS_dev_env_path, host_sln_path, "/Rebuild", "Debug"])
    else:
        subprocess.run([VS_dev_env_path, host_sln_path, "/Build", "Debug"])  # or "Release"


if __name__ == '__main__':

    # try:
    #     # First attempt
    #     load_usb(False,VID=0x04B4, PID=0x00f3) # Cypress VID when in bootloader mode
    # except Exception:
    #     try:
    #         # Second attempt
    #         load_usb(False, VID=0x04B4, PID=0x00f1)  # Cypress VID when image is loaded
    #     except Exception as e:
    #         print(f"No USB devices found: {e}")


    #Compile fw
    eclipse_exe = "C:/Program Files (x86)/Cypress/EZ-USB FX3 SDK/1.3/Eclipse/ezUsbSuite.exe"  # Adjust this path
    project_path = "C:/Users/LanaBeck/Documents/GitHub/fx3_gpif_ex2"
    compile_eclipse_project(eclipse_exe, project_path)

    #load on to FX3
    cypress_fw_prog = r"C:\Program Files (x86)\Cypress\EZ-USB FX3 SDK\1.3\util\cyfwprog\cyfwprog.exe"
    fw_path = f"{project_path}/Debug/GPIF_Example2.img"
    load_FX3_image(cypress_fw_prog,fw_path)

    #(build and) run host exe
    host_exe_path = r"C:\Users\LanaBeck\source\repos\dxf_host\Debug\Poll4FX3.exe"
    host_sln_path=r"C:\Users\LanaBeck\Documents\GitHub\dxf_host"
    VS_dev_env_path=r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE"

    # rebuild_host(VS_dev_env_path, host_sln_path, True)
    load_USB_host(host_exe_path)

    print("finished")
