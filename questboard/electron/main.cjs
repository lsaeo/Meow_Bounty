const { app, BrowserWindow, globalShortcut, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')

const DATA_DIR = path.join(process.env.APPDATA || path.join(require('os').homedir(), 'AppData', 'Roaming'), 'QuestPet')

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true })
  const defaults = {
    'hero.json': '{"name": "勇者", "level": 1, "exp": 0, "hp": 100, "maxHp": 100, "gold": 0, "streak": 0, "last_login": ""}',
    'tasks.json': '[]',
    'ai_settings.json': '{"enabled": false, "api_key": "", "api_base": "https://api.deepseek.com", "model": "deepseek-chat", "system_prompt": ""}',
  }
  for (const [name, content] of Object.entries(defaults)) {
    const p = path.join(DATA_DIR, name)
    if (!fs.existsSync(p)) fs.writeFileSync(p, content, 'utf-8')
  }
}

function readJson(filename) {
  ensureDataDir()
  const p = path.join(DATA_DIR, filename)
  if (!fs.existsSync(p)) {
    if (filename === 'hero.json')
      return { name: '勇者', level: 1, exp: 0, hp: 100, maxHp: 100, gold: 0, streak: 0, last_login: '' }
    if (filename === 'tasks.json') return []
    return null
  }
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')) } catch { return filename === 'tasks.json' ? [] : null }
}

function writeJson(filename, data) {
  ensureDataDir()
  fs.writeFileSync(path.join(DATA_DIR, filename), JSON.stringify(data, null, 2), 'utf-8')
}

let win = null

function createWindow() {
  win = new BrowserWindow({
    width: 1200, height: 800, minWidth: 900, minHeight: 600,
    frame: false, titleBarStyle: 'hidden',
    backgroundColor: '#1a0a04',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs')
    }
  })

  const isDev = process.argv.includes('--dev') || !app.isPackaged
  if (isDev) {
    win.loadURL('http://localhost:5173')
  } else {
    win.loadFile(path.join(__dirname, '..', 'dist', 'index.html'))
  }

  win.setMenuBarVisibility(false)
  globalShortcut.register('Ctrl+N', () => win?.webContents.send('open-editor'))
}

ipcMain.handle('read-json', (_, filename) => readJson(filename))
ipcMain.handle('write-json', (_, filename, data) => writeJson(filename, data))

app.whenReady().then(createWindow)
app.on('window-all-closed', () => app.quit())

ipcMain.on('minimize', () => win?.minimize())
ipcMain.on('maximize', () => { if (win?.isMaximized()) win.unmaximize(); else win?.maximize() })
ipcMain.on('close', () => win?.close())
