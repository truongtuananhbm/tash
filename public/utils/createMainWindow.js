const { BrowserWindow ,Menu} = require("electron");
const { join } = require("path");
const { autoUpdater } = require("electron-updater");
const remote = require("@electron/remote/main");
const config = require("./config");


exports.createMainWindow = async () => {


	const window = new BrowserWindow({
		minWidth: 1250,
		minHeight: 950,
		width: 1250,
		height: 950,
		webPreferences: {
			nodeIntegration: true,
			enableRemoteModule: true,
			devTools: config.isDev,
			// devTools: true,
			contextIsolation: false,
		},
		frame: true,
		autoHideMenuBar: true,
		icon: config.icon,
		title: config.appName,


	});


	remote.enable(window.webContents);

	await window.loadURL(
		config.isDev
			? "http://localhost:3000"
			: `file://${join(__dirname, "..", "../build/index.html")}`,
	);

	window.once("ready-to-show", () => {
		autoUpdater.checkForUpdatesAndNotify();
	});

	window.on("close", (e) => {
		if (!config.isQuiting) {
			// window = null
			// e.preventDefault();
			//
			// window.hide();
		}
	});

	return window;
};
