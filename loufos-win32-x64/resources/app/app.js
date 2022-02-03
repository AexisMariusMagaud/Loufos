const {app, BrowserWindow} = require('electron')
const path = require('path')
const url = require('url')
var force_quit = false;

let window = null

// Wait until the app is ready
app.once('ready', () => {
  // Create a new window
  window = new BrowserWindow({
    // Set the initial width to 800px
    width: 1000,
    // Set the initial height to 600px
    height: 1400,
    // Set the default background color of the window to match the CSS
    // background color of the page, this prevents any white flickering
    backgroundColor: "#D6D8DC",
    // Don't show the window until it's ready, this prevents any white flickering
    show: false,
    autoHideMenuBar: true


  })


  // Load a URL in the window to the local index.html path
  window.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))

  // Show window when page is ready
  window.once('ready-to-show', () => {
    window.show()
  })


  window.on('close', function(e){
    if(!force_quit){
        e.preventDefault();
        window.hide();
    }
  });

  // You can use 'before-quit' instead of (or with) the close event
  app.on('before-quit', function (e) {
    // Handle menu-item or keyboard shortcut quit here
    if(!force_quit){
        e.preventDefault();
        window.hide();
    }
  });

  // Remove mainWindow.on('closed'), as it is redundant

  app.on('activate-with-no-open-windows', function(){
    window.show();
  });


})

app.on('will-quit', function () {
  // This is a good place to add tests insuring the app is still
  // responsive and all windows are closed.
  console.log("will-quit");
  mainWindow = null;
});