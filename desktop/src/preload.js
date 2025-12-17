const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  app: {
    getPath: (name) => {
      ipcRenderer.send('app-get-path', name);
      return new Promise((resolve) => {
        ipcRenderer.once('app-path', (event, path) => {
          resolve(path);
        });
      });
    },
    getVersion: (name) => {
      ipcRenderer.send('app-get-version');
      return new Promise((resolve) => {
        ipcRenderer.once('app-version', (event, version) => {
          resolve(version);
        });
      });
    },
    minimize: () => ipcRenderer.send('app-minimize'),
    maximize: () => ipcRenderer.send('app-maximize'),
    close: () => ipcRenderer.send('app-close'),
    on: (channel, func) => {
      const validChannels = ['app-info', 'navigate', 'show-about'];
      if (validChannels.includes(channel)) {
        ipcRenderer.on(channel, (event, ...args) => func(...args));
      }
    }
  }
});
