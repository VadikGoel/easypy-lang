[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{EASYPY-LANG-V2-ENGINE}}
AppName=Easypy Language Engine
AppVersion=2.0
AppPublisher=Easypy Team
AppPublisherURL=https://github.com/
DefaultDirName={userpf}\Easypy
DisableProgramGroupPage=yes
OutputBaseFilename=Easypy_Installer_v2
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Copy the entire source code to the install directory
Source: "..\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
; Run the pip install command after copying files
; usage: python -m pip install -e .
Filename: "cmd.exe"; Parameters: "/C pip install -r ""{app}\requirements.txt"""; StatusMsg: "Installing dependencies (requests, numpy, etc)..."; Flags: runhidden
Filename: "cmd.exe"; Parameters: "/C pip install -e ""{app}"""; StatusMsg: "Registering Easypy engine..."; Flags: runhidden

[Messages]
FinishedHeadingLabel=Installation Complete!
FinishedLabel=Easypy has been successfully installed on your computer. An 'easypy' command is now available in your terminal. 

[Code]
// Simple check to warn if Python is not found (Optional advanced feature)
