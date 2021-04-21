; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "ImaGC"
#define MyAppVersion "0.2-022021"
#define MyAppPublisher "ArtesGC, Inc."
#define MyAppURL "http://artesgc.home.blog/"
#define MyAppExeName "ImaGC.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{DDB3572B-F365-49E9-AA82-8F95F4F499E1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
VersionInfoCompany={#MyAppPublisher}
VersionInfoCopyright="2019-2021 Nurul Carvalho"
VersionInfoDescription="Editor de imagens"
VersionInfoOriginalFileName={#MyAppName}
VersionInfoProductName={#MyAppName}
VersionInfoProductTextVersion={#MyAppVersion}
; VersionInfoProductVersion={#MyAppVersion}
; VersionInfoVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DefaultUserInfoName={#MyAppName}
DefaultUserInfoOrg={#MyAppPublisher}
DisableProgramGroupPage=yes
LicenseFile=D:\Projectos\ArtesGC\GC-LicensasOS\license_free(pt).txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=D:\Projectos\ImaGC\dist
OutputBaseFilename=ImaGC
SetupIconFile=D:\Projectos\ImaGC\ImaGC-ico\imagc-256x256.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\Projectos\ImaGC\ImaGC.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Projectos\ImaGC\img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs
Source: "D:\Projectos\ArtesGC\GC-LicensasOS\license_free(pt).txt"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

