const { contextBridge, ipcRenderer } = require('electron')
contextBridge.exposeInMainWorld('api', {
  readJson: (filename) => ipcRenderer.invoke('read-json', filename),
  writeJson: (filename, data) => ipcRenderer.invoke('write-json', filename, data),
  minimize: () => ipcRenderer.send('minimize'),
  maximize: () => ipcRenderer.send('maximize'),
  close: () => ipcRenderer.send('close'),
  onOpenEditor: (cb) => ipcRenderer.on('open-editor', cb),
})
