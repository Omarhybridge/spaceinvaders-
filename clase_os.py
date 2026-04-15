import os
current_directory = os.getcwd()
print("Directorio actual:", current_directory)

new_directory = os.path.join(current_directory, "nuevo_directorio")


os.mkdir(new_directory)
print("Directorio creado:", new_directory)
files_in_directory = os.listdir(current_directory)
print("Archivos en el directorio:", files_in_directory)
