const { app, ipcMain } = require('electron');

const createTitlebar = (window) => {
  const titlebarHtml = `
    <style>
      #titlebar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 32px;
        background: linear-gradient(90deg, #0a0e27 0%, #1a1f3a 100%);
        border-bottom: 1px solid #333;
        -webkit-user-select: none;
        user-select: none;
        -webkit-app-region: drag;
        font-size: 12px;
        color: #e0e0e0;
        padding: 0 10px;
      }

      #titlebar-title {
        flex: 1;
        padding-left: 10px;
        font-weight: 500;
        color: #7cffb2;
      }

      .titlebar-button {
        -webkit-app-region: no-drag;
        width: 36px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: none;
        background: transparent;
        color: #e0e0e0;
        font-size: 18px;
        transition: background-color 0.2s;
      }

      .titlebar-button:hover {
        background-color: rgba(124, 255, 178, 0.1);
      }

      .titlebar-button:active {
        background-color: rgba(124, 255, 178, 0.2);
      }

      #titlebar-close:hover {
        background-color: #ff6b6b;
        color: white;
      }
    </style>

    <div id="titlebar">
      <div id="titlebar-title">Valyxo v0.41</div>
      <div style="display: flex; gap: 2px;">
        <button class="titlebar-button" id="titlebar-minimize">−</button>
        <button class="titlebar-button" id="titlebar-maximize">□</button>
        <button class="titlebar-button" id="titlebar-close">✕</button>
      </div>
    </div>
  `;

  window.webContents.on('did-finish-load', () => {
    window.webContents.executeJavaScript(`
      if (!document.getElementById('titlebar')) {
        const titlebar = document.createElement('div');
        titlebar.innerHTML = \`${titlebarHtml}\`;
        document.body.insertBefore(titlebar.firstChild, document.body.firstChild);

        document.getElementById('titlebar-minimize').addEventListener('click', () => {
          require('electron').ipcRenderer.send('app-minimize');
        });

        document.getElementById('titlebar-maximize').addEventListener('click', () => {
          require('electron').ipcRenderer.send('app-maximize');
        });

        document.getElementById('titlebar-close').addEventListener('click', () => {
          require('electron').ipcRenderer.send('app-close');
        });
      }
    `);
  });
};

module.exports = createTitlebar;
