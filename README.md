## Programación empleada en mi TFG de ASIR: "Sistema de Almacenamiento en una Nube Privada con Enfoque en Seguridad y Respaldo Incremental Automatizado".

Este proyecto se trata de una aplicación web desarrollada con Django para gestionar usuarios FTP. La aplicación permite registrar nuevos usuarios, autenticar su acceso y subir archivos a sus directorios personales en un servidor FTP. La gestión del servidor FTP se realiza mediante comandos SSH.

### Contenidos

1. [Funcionalidades](#funcionalidades)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Capturas](#capturas)
5. [Licencia](#licencia)

### Funcionalidades

- **Registro de Usuarios**: Los usuarios pueden registrarse proporcionando su información personal. Al registrarse, se crean automáticamente sus directorios personales en el servidor FTP con los permisos adecuados.
- **Autenticación**: Los usuarios pueden iniciar sesión con sus credenciales para acceder a sus directorios FTP.
- **Subida de Archivos**: Los usuarios pueden subir archivos a sus directorios personales en el servidor FTP. Los archivos subidos son propiedad del usuario y del grupo ftpusers.
- **Gestión de Permisos**: La aplicación asegura que los directorios y archivos en el servidor FTP tengan los permisos correctos.

### Tecnologías Utilizadas

- **Django**: Framework web utilizado para el desarrollo de la aplicación.
- **Paramiko**: Biblioteca Python para realizar conexiones SSH.
- **pysftp**: Biblioteca Python para gestionar las transferencias de archivos SFTP.

### Estructura del Proyecto

#### 1. Formulario de Registro

- **Formulario de Usuario (UserForm)**: Permite a los usuarios ingresar su información personal para registrarse.
- **Formulario de Perfil de Usuario (UserProfileForm)**: Permite a los usuarios ingresar información adicional para su perfil.

#### 2. Vistas

- **Registro (register)**: Procesa el registro de nuevos usuarios, crea sus directorios en el servidor FTP y configura los permisos adecuados.
- **Inicio de Sesión (login)**: Permite a los usuarios iniciar sesión.
- **Página Principal (home)**: Página de inicio después de iniciar sesión.
- **Cierre de Sesión (logout)**: Permite a los usuarios cerrar sesión.
- **Subida de Archivos (upload_file)**: Permite a los usuarios subir archivos a sus directorios FTP.

#### 3. Utilidades

- **Comandos SSH (execute_ssh_commands)**: Ejecuta comandos en el servidor FTP para gestionar usuarios y permisos.
- **Subida de Archivos SFTP (sftp_upload_file)**: Gestiona la subida de archivos al servidor FTP usando SFTP.

### Capturas

![register](https://github.com/SergioPinilla04/TFG_ASIR2024/assets/113448338/d82181f2-420a-4e3c-b1f2-035be81e4808)
![login](https://github.com/SergioPinilla04/TFG_ASIR2024/assets/113448338/3f07dd7c-858a-4786-b1a0-636bdce161c5)
![upload](https://github.com/SergioPinilla04/TFG_ASIR2024/assets/113448338/114745df-e082-47e7-a57a-888a7a0b5eb1)

### Licencia

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/SergioPinilla04/TFG_ASIR2024">Sistema de Almacenamiento en una Nube Privada con Enfoque en Seguridad y Respaldo Incremental Automatizado</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/SergioPinilla04">Sergio Pinilla</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p>
