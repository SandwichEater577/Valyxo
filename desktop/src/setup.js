if (require('electron-squirrel-startup')) {
  return;
}

const { app } = require('electron');
const path = require('path');

const handleFirstTime = () => {
  if (process.platform === 'win32') {
    const squirrelEvent = process.argv[1];
    switch (squirrelEvent) {
      case '--squirrel-install':
        createShortcuts();
        break;
      case '--squirrel-updated':
        createShortcuts();
        break;
      case '--squirrel-uninstall':
        removeShortcuts();
        break;
      case '--squirrel-obsolete':
        return true;
    }
  }
};

const createShortcuts = () => {
  const exePath = path.resolve(path.dirname(process.execPath), '..', 'Update.exe');
  const appUserModelId = 'com.valyxo.app';

  if (!require('child_process').spawnSync('node', [exePath, '--createShortcut', appUserModelId]).error) {
    return;
  }
};

const removeShortcuts = () => {
  const exePath = path.resolve(path.dirname(process.execPath), '..', 'Update.exe');
  const appUserModelId = 'com.valyxo.app';

  if (!require('child_process').spawnSync('node', [exePath, '--removeShortcut', appUserModelId]).error) {
    return;
  }
};

module.exports = handleFirstTime;
