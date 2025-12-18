const {
  app,
  BrowserWindow,
  Menu,
  ipcMain,
  Tray,
  nativeTheme,
} = require("electron");
const path = require("path");
const fs = require("fs");
const isDev = !app.isPackaged;

let mainWindow;
let tray;

// Website path for loading the local website
const getWebsitePath = () => {
  if (isDev) {
    return path.join(__dirname, "../../website/HTML");
  }
  return path.join(process.resourcesPath, "website/HTML");
};

const createWindow = () => {
  const iconPath = path.join(__dirname, "../assets/icon.png");
  const windowConfig = {
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
    },
  };

  if (fs.existsSync(iconPath)) {
    windowConfig.icon = iconPath;
  }

  mainWindow = new BrowserWindow(windowConfig);

  mainWindow.webContents.userAgent = "Valyxo/0.5.1 (Desktop)";

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  mainWindow.on("minimize", () => {
    mainWindow.hide();
  });

  mainWindow.webContents.on("did-finish-load", () => {
    mainWindow.webContents.send("app-info", {
      version: app.getVersion(),
      platform: process.platform,
      isDesktopApp: true,
    });
  });
};

const loadApplication = async () => {
  createWindow();

  const websitePath = getWebsitePath();
  const indexPath = path.join(websitePath, "index.html");

  mainWindow.loadFile(indexPath);
};

const createTray = () => {
  try {
    const iconPath = path.join(__dirname, "../assets/icon-small.png");
    if (!fs.existsSync(iconPath)) {
      console.warn("Icon file not found, skipping tray creation");
      return;
    }
    tray = new Tray(iconPath);

    const contextMenu = Menu.buildFromTemplate([
      {
        label: "Show",
        click: () => {
          if (mainWindow) {
            mainWindow.show();
          } else {
            loadApplication();
          }
        },
      },
      {
        label: "Dashboard",
        click: () => {
          if (mainWindow) {
            const websitePath = getWebsitePath();
            mainWindow.loadFile(path.join(websitePath, "dashboard.html"));
            mainWindow.show();
          }
        },
      },
      {
        label: "Projects",
        click: () => {
          if (mainWindow) {
            const websitePath = getWebsitePath();
            mainWindow.loadFile(path.join(websitePath, "projects.html"));
            mainWindow.show();
          }
        },
      },
      {
        label: "Documentation",
        click: () => {
          if (mainWindow) {
            const websitePath = getWebsitePath();
            mainWindow.loadFile(path.join(websitePath, "docs.html"));
            mainWindow.show();
          }
        },
      },
      { type: "separator" },
      {
        label: "Settings",
        click: () => {
          if (mainWindow) {
            const websitePath = getWebsitePath();
            mainWindow.loadFile(path.join(websitePath, "settings.html"));
            mainWindow.show();
          }
        },
      },
      {
        label: "About",
        click: () => {
          if (mainWindow) {
            mainWindow.webContents.send("show-about");
          }
        },
      },
      { type: "separator" },
      {
        label: "Exit",
        click: () => {
          app.quit();
        },
      },
    ]);

    tray.setContextMenu(contextMenu);
    tray.setToolTip("Valyxo");
    tray.on("double-click", () => {
      if (mainWindow) {
        mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
      }
    });
  } catch (error) {
    console.error("Failed to create tray:", error);
  }
};

const createMenu = () => {
  const template = [
    {
      label: "File",
      submenu: [
        {
          label: "Exit",
          accelerator: "CmdOrCtrl+Q",
          click: () => {
            app.quit();
          },
        },
      ],
    },
    {
      label: "Edit",
      submenu: [
        { role: "undo" },
        { role: "redo" },
        { type: "separator" },
        { role: "cut" },
        { role: "copy" },
        { role: "paste" },
      ],
    },
    {
      label: "View",
      submenu: [
        { role: "reload" },
        { role: "forceReload" },
        { role: "toggleDevTools" },
        { type: "separator" },
        { role: "resetZoom" },
        { role: "zoomIn" },
        { role: "zoomOut" },
        { type: "separator" },
        { role: "togglefullscreen" },
      ],
    },
    {
      label: "Tools",
      submenu: [
        {
          label: "Documentation",
          click: () => {
            if (mainWindow) {
              const websitePath = getWebsitePath();
              mainWindow.loadFile(path.join(websitePath, "docs.html"));
            }
          },
        },
        {
          label: "API Reference",
          click: () => {
            if (mainWindow) {
              const websitePath = getWebsitePath();
              mainWindow.loadFile(path.join(websitePath, "api.html"));
            }
          },
        },
        {
          label: "Changelog",
          click: () => {
            if (mainWindow) {
              const websitePath = getWebsitePath();
              mainWindow.loadFile(path.join(websitePath, "changelog.html"));
            }
          },
        },
      ],
    },
    {
      label: "Help",
      submenu: [
        {
          label: "About Valyxo",
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.send("show-about");
            }
          },
        },
        {
          label: "Website",
          click: () => {
            if (mainWindow) {
              const websitePath = getWebsitePath();
              mainWindow.loadFile(path.join(websitePath, "index.html"));
            }
          },
        },
      ],
    },
  ];

  if (isDev) {
    template.push({
      label: "Development",
      submenu: [{ role: "toggleDevTools" }],
    });
  }

  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
};

ipcMain.on("app-get-path", (event, name) => {
  event.reply("app-path", app.getPath(name));
});

ipcMain.on("app-get-version", (event) => {
  event.reply("app-version", app.getVersion());
});

ipcMain.on("app-minimize", () => {
  if (mainWindow) mainWindow.minimize();
});

ipcMain.on("app-maximize", () => {
  if (mainWindow) {
    mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize();
  }
});

ipcMain.on("app-close", () => {
  app.quit();
});

app.on("ready", async () => {
  if (process.platform === "win32" && app.isPackaged) {
    const squirrelEvent = require("electron-squirrel-startup");
    if (squirrelEvent) {
      app.quit();
    }
  }

  await loadApplication();
  createMenu();
  createTray();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    loadApplication();
  } else {
    mainWindow.show();
  }
});

app.on("quit", () => {
  // Cleanup on quit
});

if (isDev) {
  try {
    require("electron-reloader")(module);
  } catch (e) {
    console.log("Electron reloader not available");
  }
}
