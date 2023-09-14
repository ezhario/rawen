<p align="center">
  <img width="99" height="125" src="https://images.plurk.com/6QOnj9PXofQKxSyrTgibNV.png" alt="App Icon"/>
</p>

# What's this?
Rawen is an app written in Python with wxPython as GUI toolkit.
Main and the only funtion is removing the redundant RAW files who don't 
have corresponding JPG's from Camera SD Cards.
<p align="center">
  <img width="512" height="362" src="https://images.plurk.com/6cfoEnPk4kZSZd45321b4I.png" alt="App main (and only) window"/>
</p>
Usage scenario:
1. Make some photos
2. Extract the SD Card from your Camera and insert it to your Mac
3. Check the JPGs with Preview and remove the photos you don't like
4. Run Rawen.app, open SD Card in it. Rawen will count and show, how many 
RAWs and JPGs you have.
5. Press 'Do it.'. Rawen will delete the RAWs which has no JPGs with the 
same name in one folder. 

Please note: RAW removal cannot be undone (easily) and I'm not responsible for any data loss.

# Building instructions
## 1. Install required packages:
```
pip3 install -r requirements.txt
```

## 2. Install DMG creation tool:
```
brew install create-dmg
```

## 3. Create an app:
```
pyinstaller --name 'Rawen' \
            --icon 'AppIcon.icns' \
            --windowed  \
            rawen.py
```

## 4. Create a directory for a DMG file:
```
mkdir -p dist/dmg
```

## 5. Copy .app to dmg folder:
```
cp -r "dist/Rawen.app" dist/dmg
```

## 6. Create DMG:
```
create-dmg \
  --volname "Rawen" \
  --volicon "rawen.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Rawen.app" 175 120 \
  --hide-extension "Rawen.app" \
  --app-drop-link 425 120 \
  "dist/Rawen.dmg" \
  "dist/dmg/"
```

## 7. Enjoy.
Find your `Rawen.dmg` file in the `dist` folder.
