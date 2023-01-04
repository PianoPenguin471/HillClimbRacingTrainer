import pymem
import customtkinter
from pymem.ptypes import RemotePointer
import keyboard


COIN_ADDRESS = 0x28CAD4
GEM_ADDRESS = 0x28CAD4
GAS_BASE = 0x28CA2C
GAS_OFFSET = 0x2A8

"""
Multilevel pointers
def getPointerAddress(base, offsets):
    remote_pointer = RemotePointer(hill_climb_racing.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(hill_climb_racing.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset
"""

hill_climb_racing = None
while hill_climb_racing is None:
    try:
        hill_climb_racing = pymem.Pymem("HillClimbRacing.exe")
        print(hill_climb_racing)
    except Exception:
        continue


def get_gas_address():
    remote_ptr = RemotePointer(hill_climb_racing.process_handle, hill_climb_racing.base_address + GAS_BASE)
    return remote_ptr.value + GAS_OFFSET


root = customtkinter.CTk()
print(hill_climb_racing)
root.geometry("300x250")
root.title("Hill Climb Racing Cheat")
root.minsize(300, 250)
root.attributes('-topmost', 1)
root.iconbitmap("C:\\Users\\danie\\OneDrive\\Documents\\Hill Climb Racing Cheat\\src\\car.ico")

# create 2x2 grid system
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure((0, 1), weight=1)

customtkinter.set_default_color_theme("green")


def clean_entry(entry_data: str) -> int:
    if not entry_data.isdecimal():
        return 123456
    num_value = int(entry_data)
    if num_value > 2147483647:
        num_value = 214783647
    return num_value


coin_entry = customtkinter.CTkEntry(master=root, placeholder_text="Enter Coin Amount Here")
coin_entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")


def set_coins():
    hill_climb_racing.write_int(hill_climb_racing.base_address + COIN_ADDRESS, clean_entry(coin_entry.get()))


coin_button = customtkinter.CTkButton(master=root, text="Set Coins", command=set_coins)
coin_button.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

gem_entry = customtkinter.CTkEntry(master=root, placeholder_text="Enter Gem Amount Here")
gem_entry.grid(row=1, column=0, padx=20, pady=20, sticky="ew")


def set_gems():
    hill_climb_racing.write_int(hill_climb_racing.base_address + GEM_ADDRESS, clean_entry(gem_entry.get()))


gem_button = customtkinter.CTkButton(master=root, text="Set Gems", command=set_gems(), state="disabled") # TODO: fix gem address and button state
gem_button.grid(row=1, column=1, padx=20, pady=40, sticky="ew")


def reset_gas():
    address = get_gas_address()
    if address == 0x2A8:
        print('Only reset gas when in a "race"!')
        return
    hill_climb_racing.write_float(address, float(100))


is_hidden = False


def hide_window():
    global is_hidden
    is_hidden = not is_hidden
    if is_hidden:
        root.withdraw()
    else:
        root.iconify()


reset_gas_button = customtkinter.CTkButton(master=root, text="Reset Gas", command=reset_gas)
reset_gas_button.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
keyboard.add_hotkey('ctrl+g', reset_gas)
keyboard.add_hotkey('ctrl+i', hide_window)
root.mainloop()
