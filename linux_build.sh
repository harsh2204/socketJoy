# Build instructions
# Ensure that you've installed the following
# * pyinstaller 
# * pip install -r socketjoy/requirements.txt
# * appimagetool
[[ $(type -P appimagetool) ]] && echo "appimagetool found"  || { echo "appimagetool not found" 1>&2; exit 1; }
[[ $(type -P pyinstaller) ]] && echo "pyinstaller found"  || { echo "pyinstaller not found" 1>&2; exit 1; }

rm -rf dist/socketjoy

pyinstaller --clean -y socketjoy.spec
appimagetool dist/socketjoy/ dist/socketJoy.AppImage