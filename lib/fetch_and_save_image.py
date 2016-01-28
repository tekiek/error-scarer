from preprocess import preprocess

loadedImage = preprocess.loadScaledImage(
    'http://freedwallpaper.com/wp-content/uploads/2014/11/cat-wallpaper-free-download-8796.jpg', 350, 350, True)
# loadedImage = preprocess.loadScaledNdArray('http://freedwallpaper.com/wp-content/uploads/2014/11/cat-wallpaper-free-download-8796.jpg', 350, 350, True)


loadedImage.save('grey_and_scaled.png')
