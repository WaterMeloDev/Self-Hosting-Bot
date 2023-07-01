import customtkinter
import subprocess
import signal

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# create the main application window
root = customtkinter.CTk()
root.title('Self-Hosting Panel')
root.geometry("500x500")

# store the bot process
bot_process = None

def run_bot(token_entry):
    global bot_process
    try:
        bot_token = token_entry.get()
        bot_process = subprocess.Popen(["python3", "/home/watermelo/Python-Panel/Panel/bot/commands.py", bot_token])
        update_status_label("Success: Your bot is now online.")
    except:
        update_status_label("Error: improper token passed.")

def stop_bot():
    global bot_process
    if bot_process is not None:
        bot_process.send_signal(signal.SIGINT)
        update_status_label("Bot stopped.")
        bot_process = None
    else:
        update_status_label("No bot is currently running.")

def update_status_label(status_text):
    status_label.configure(text=status_text)
    root.after(3000, lambda: status_label.configure(text=""))  # Clear the label after 3000ms (3 seconds)

# create the GUI elements
frame = customtkinter.CTkFrame(master=root, bg_color='black')
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Bot System", font=("Arial", 16))
label.pack(pady=12, padx=10)

token = customtkinter.CTkEntry(master=frame, placeholder_text="Bot Token", show="*", font=("Arial", 12))
token.pack(pady=12, padx=10)

button_Run = customtkinter.CTkButton(master=frame, text="Run", command=lambda: run_bot(token), fg_color='green', font=("Arial", 12))
button_Run.pack(pady=12, padx=10)

button_Stop = customtkinter.CTkButton(master=frame, text="Stop", command=stop_bot, fg_color='red', font=("Arial", 12))
button_Stop.pack(pady=12, padx=10)

# Status label to display success/error messages
status_label = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 12))
status_label.pack(pady=12, padx=10)

# start the application
root.mainloop()
