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
const { spawn } = require("child_process");
const isDev = !app.isPackaged;

let mainWindow;
let tray;
let serverProcess;
let serverReady = false;

const SERVER_PORT = 5000;
const SERVER_HOST = "http://localhost:5000";

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

  mainWindow.webContents.userAgent = "Valyxo/0.41.0 (Desktop)";

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
      server: SERVER_HOST,
    });
  });
};

const startBackendServer = async () => {
  return new Promise((resolve, reject) => {
    const serverPath = path.join(__dirname, "../../server/src/server.js");

    if (!fs.existsSync(serverPath)) {
      console.error("Server file not found:", serverPath);
      reject(new Error("Backend server not found"));
      return;
    }

    serverProcess = spawn("node", [serverPath], {
      env: {
        ...process.env,
        NODE_ENV: isDev ? "development" : "production",
        PORT: SERVER_PORT,
        DB_PATH: path.join(app.getPath("userData"), "valyxo.db"),
      },
      detached: false,
      stdio: ["ignore", "pipe", "pipe"],
    });

    serverProcess.stdout.on("data", (data) => {
      console.log(`[Backend] ${data.toString().trim()}`);
    });

    serverProcess.stderr.on("data", (data) => {
      console.error(`[Backend Error] ${data.toString().trim()}`);
    });

    serverProcess.on("error", (err) => {
      console.error("Failed to start backend server:", err);
      reject(err);
    });

    let attempts = 0;
    const checkServer = setInterval(() => {
      attempts++;

      fetch(`${SERVER_HOST}/health`)
        .then(() => {
          clearInterval(checkServer);
          serverReady = true;
          console.log("Backend server is ready");
          resolve();
        })
        .catch(() => {
          if (attempts > 30) {
            clearInterval(checkServer);
            reject(new Error("Backend server failed to start"));
          }
        });
    }, 500);

    setTimeout(() => {
      clearInterval(checkServer);
      if (!serverReady) {
        reject(new Error("Backend server startup timeout"));
      }
    }, 15000);
  });
};

const loadApplication = async () => {
  if (isDev) {
    await startBackendServer().catch((err) => {
      console.error("Failed to start backend:", err);
      app.quit();
    });
  }

  createWindow();

  mainWindow.loadURL(`${SERVER_HOST}`);
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
          mainWindow.webContents.send("navigate", "/dashboard.html");
          mainWindow.show();
        }
      },
    },
    {
      label: "Projects",
      click: () => {
        if (mainWindow) {
          mainWindow.webContents.send("navigate", "/projects.html");
          mainWindow.show();
        }
      },
    },
    {
      label: "API Docs",
      click: () => {
        if (mainWindow) {
          mainWindow.webContents.send("navigate", `${SERVER_HOST}/api-docs`);
          mainWindow.show();
        }
      },
    },
    { type: "separator" },
    {
      label: "Settings",
      click: () => {
        if (mainWindow) {
          mainWindow.webContents.send("navigate", "/settings.html");
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
          label: "API Documentation",
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.loadURL(`${SERVER_HOST}/api-docs`);
            }
          },
        },
        {
          label: "Server Health",
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.loadURL(`${SERVER_HOST}/health`);
            }
          },
        },
        {
          label: "Metrics",
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.loadURL(`${SERVER_HOST}/metrics`);
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
          label: "Documentation",
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.loadURL(`${SERVER_HOST}/docs.html`);
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
  if (serverProcess) {
    serverProcess.kill();
  }
});

if (isDev) {
  try {
    require("electron-reloader")(module);
  } catch (e) {
    console.log("Electron reloader not available");
  }
}
