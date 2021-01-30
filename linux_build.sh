rm -rf dist/socketjoy
pyinstaller --clean -y socketjoy.spec
appimagetool dist/socketjoy/ dist/socketJoy.AppImage