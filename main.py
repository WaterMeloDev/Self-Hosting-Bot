# import necessary modules
import subprocess
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme('dark-blue')

# create the main application window
root = customtkinter.CTk()
root.title('Self-Hosting Launch')
root.geometry("500x500")

# function to handle the launch process
def launch_app():
    print("Launch successful")

    # launch main.py from the "Panel" folder
    subprocess.Popen(["python3", "Panel/panel.py"])

    # close the current application window
    root.destroy()

# create the GUI elements
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Do you wish to launch the app?")
label.pack(pady=12, padx=10)

button_launch = customtkinter.CTkButton(master=frame, text="Launch", command=launch_app)
button_launch.pack(pady=12, padx=10)


# start the application
root.mainloop()
