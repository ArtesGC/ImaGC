; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "imagc"
#define MyAppVersion "1.0"
#define MyAppPublisher "ArtesGC, Inc."
#define MyAppURL "https://artesgc.github.io/ImaGC"
#define MyAppExeName "imagc.exe"

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
VersionInfoCopyright="(c) 2020-2022 Nurul Carvalho"
VersionInfoDescription="An easy way to add logos to your images or convert to ico"
VersionInfoOriginalFileName={#MyAppName}
VersionInfoProductName={#MyAppName}
VersionInfoProductTextVersion={#MyAppVersion}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoTextVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DefaultUserInfoName={#MyAppName}
DefaultUserInfoOrg={#MyAppPublisher}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
; PrivilegesRequiredOverridesAllowed=dialog
OutputDir=..\dist
OutputBaseFilename={#MyAppName}_{#MyAppVersion}-052022_amd64
SetupIconFile=..\imagc\ima-icons\favicon-256x256.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl";
Name: "english"; MessagesFile: "compiler:Default.isl";

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\imagc.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\imagc\ima-icons\*"; DestDir: "{app}\ima-icons"; Flags: ignoreversion recursesubdirs
Source: "..\imagc\ima-themes\*"; DestDir: "{app}\ima-themes"; Flags: ignoreversion recursesubdirs
Source: "..\imagc\ima-fonts\*"; DestDir: "{app}\ima-fonts"; Flags: ignoreversion recursesubdirs
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

