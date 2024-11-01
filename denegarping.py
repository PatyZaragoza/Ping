import tkinter as tk
from tkinter import messagebox
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el comando: {e.stderr.decode()}")

def check_rule_exists(command):
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def allow_ping(ips):
    for ip in ips:
        # Verificar si la regla de denegación existe
        check_command = f"sudo iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
        if check_rule_exists(check_command):
            # Eliminar la regla de denegación si existe
            command = f"sudo iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
            run_command(command)
        
        # Agregar la regla de aceptación
        command = f"sudo iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
        run_command(command)
        print(f"Ping permitido desde la IP {ip}")

def deny_ping(ips):
    for ip in ips:
        # Verificar si la regla de aceptación existe
        check_command = f"sudo iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
        if check_rule_exists(check_command):
            # Eliminar la regla de aceptación si existe
            command = f"sudo iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
            run_command(command)
        
        # Agregar la regla de denegación
        command = f"sudo iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
        run_command(command)
        print(f"Ping denegado desde la IP {ip}")

def execute_action(action):
    ip = ip_entry.get()  # Obtener la IP del cuadro de texto
    if ip:
        if action == 'permitir':
            allow_ping([ip])  # Pasar la IP como lista
            messagebox.showinfo("Acción completada", f"Ping permitido desde la IP {ip}.")
        elif action == 'denegar':
            deny_ping([ip])  # Pasar la IP como lista
            messagebox.showinfo("Acción completada", f"Ping denegado desde la IP {ip}.")
        else:
            messagebox.showerror("Error", "Acción no válida.")
    else:
        messagebox.showerror("Error", "Por favor, ingresa una dirección IP.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("PINGS")
root.geometry("400x250")

action_label = tk.Label(root, text="¿Quieres permitir o denegar el ping?")
action_label.pack(pady=10)

action_variable = tk.StringVar(root)
action_variable.set("Seleccione la accion")  # Valor por defecto

action_menu = tk.OptionMenu(root, action_variable, "permitir", "denegar")
action_menu.pack(pady=10)

ip_label = tk.Label(root, text="Ingresa la dirección IP:")
ip_label.pack(pady=10)

ip_entry = tk.Entry(root)  # Cuadro de texto para la dirección IP
ip_entry.pack(pady=10)

execute_button = tk.Button(root, text="Ejecutar", command=lambda: execute_action(action_variable.get()))
execute_button.pack(pady=10)

root.mainloop()
