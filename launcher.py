# Import libraries
import sys
import json
import subprocess
from PyQt5.QtWidgets import *

# Grab current settings from index
with open('data/parameters/index.json') as file:
    content = json.load(file)
    launchParameters = content['launchParameters']
    width = launchParameters['width']
    height = launchParameters['height']
    antiAliasing = launchParameters['antiAliasing']
    potatoMode = launchParameters['potatoMode']
    skipIntro = launchParameters['skipIntro']
    skipCountdown = launchParameters['skipCountdown']
    
    # String formatting
    resolutionStr = str(width) + 'x' + str(height)

# Launcher
class launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.startGui()
    
    def startGui(self):
        # Set window properties
        self.setWindowTitle('yfE')
        self.setFixedSize(200, 120)
        
        # GUI
        self.resolutionLabel = QLabel('Resolution: ')
        self.resolutionComboBox = QComboBox()
        
        supportedResolutions = ['1024x576', '1280x720', '1360x768', 
                                '1600x900', '1920x1080', '2160x1440']
        
        for res in supportedResolutions:
            self.resolutionComboBox.addItem(res)
        
        for res in supportedResolutions:
            if resolutionStr == res:
                self.resolutionComboBox.setCurrentText(res)
                
        resolutionLayout = QHBoxLayout()
        resolutionLayout.addWidget(self.resolutionLabel)
        resolutionLayout.addWidget(self.resolutionComboBox)
        
        self.antiAliasingCheckbox = QCheckBox('Anti-Aliasing')
        self.potatoModeCheckBox = QCheckBox('Low Graphics')
        upperCheckBoxLayout = QHBoxLayout()
        upperCheckBoxLayout.addWidget(self.antiAliasingCheckbox)
        upperCheckBoxLayout.addWidget(self.potatoModeCheckBox)
        
        self.skipIntroCheckbox = QCheckBox('Skip intro')
        self.skipCountdownCheckbox = QCheckBox('Skip countdown')
        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.skipIntroCheckbox)
        checkBoxLayout.addWidget(self.skipCountdownCheckbox)
        
        if antiAliasing:
            self.antiAliasingCheckbox.setChecked(True)
        else:
            self.antiAliasingCheckbox.setChecked(False)
        
        if potatoMode:
            self.potatoModeCheckBox.setChecked(True)
        else:
            self.potatoModeCheckBox.setChecked(False)
        
        if skipIntro:
            self.skipIntroCheckbox.setChecked(True)
        else:
            self.skipIntroCheckbox.setChecked(False)
        
        if skipCountdown:
            self.skipCountdownCheckbox.setChecked(True)
        else:
            self.skipCountdownCheckbox.setChecked(False)
        
        self.launchButton = QPushButton('Launch')
        self.launchButton.clicked.connect(self.launch)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.launchButton)
        
        layout = QVBoxLayout()
        layout.addLayout(resolutionLayout)
        layout.addLayout(upperCheckBoxLayout)
        layout.addLayout(checkBoxLayout)
        layout.addLayout(buttonLayout)
        
        self.setLayout(layout)
    
    def launch(self):
        # Grab UI values
        launcherResStr = self.resolutionComboBox.currentText()
        launcherAntiAlias = self.antiAliasingCheckbox.isChecked()
        launcherPotatoMode = self.potatoModeCheckBox.isChecked()
        launcherSkipIntro = self.skipIntroCheckbox.isChecked()
        launcherSkipCountdown = self.skipCountdownCheckbox.isChecked()
        
        # Format resolution and framerate into integers
        launcherResW, launcherResH = map(int, launcherResStr.split('x'))
        
        # Print launch options on console
        print('yfEngine Launcher\n')
        print('Launching with the following settings:')
        print(f' => Resolution: {launcherResStr}')
        print(f' => Anti-Aliasing: {launcherAntiAlias}')
        print(f' => Potato Mode: {launcherPotatoMode}')
        print(f' => Skip intro: {launcherSkipIntro}')
        print(f' => Skip countdown: {launcherSkipCountdown}\n')
        
        # Insert data into JSON
        content['launchParameters']['width'] = launcherResW
        content['launchParameters']['height'] = launcherResH
        content['launchParameters']['antiAliasing'] = launcherAntiAlias
        content['launchParameters']['potatoMode'] = launcherPotatoMode
        content['launchParameters']['skipIntro'] = launcherSkipIntro
        content['launchParameters']['skipCountdown'] = launcherSkipCountdown
        
        with open('data/parameters/index.json', 'w') as file:
            json.dump(content, file, indent=4)
            print('Settings saved.\n')
        
        # Run game
        game = 'engine.exe'
        subprocess.run(game)

# Run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = launcher()
    window.show()
    sys.exit(app.exec_())

# writen by markprower