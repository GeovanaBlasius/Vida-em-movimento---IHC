[Setup]
AppName=Vida em Movimento
AppVersion=1.0
AppPublisher=Geovana Blasius
AppPublisherURL=https://github.com
DefaultDirName={autopf}\Vida em Movimento
DefaultGroupName=Vida em Movimento
OutputDir=instaladores
OutputBaseFilename=VidaEmMovimento-Setup-Windows
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Area de Trabalho"; GroupDescription: "Icones adicionais:"; Flags: checkedonce

[Files]
Source: "dist\VidaEmMovimento\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Vida em Movimento"; Filename: "{app}\VidaEmMovimento.exe"
Name: "{group}\Desinstalar Vida em Movimento"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Vida em Movimento"; Filename: "{app}\VidaEmMovimento.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\VidaEmMovimento.exe"; Description: "Iniciar Vida em Movimento agora"; Flags: nowait postinstall skipifsilent
