async def get_sinfo(self,ctx,dmr):
  if dmr == None:
    mdata = {"name": None, "icon": None, "length": None, "volume": None}
    xdata = {"dmr": None, "method": None, "content": None, "playlist": None, "target": None, "cd": None, "mdata": mdata}
    return xdata
  else:
    dmr = dmr.split("@")
    method = dmr[0]
    content = dmr[1]
    playlist = None
    target = None
    cd = False
    if "playlist=" in content:
      playlist = content.split("=")[1].split(";")[0]
      target = content.split("=")[1].split(";")[1]
    if content.startswith("cd?"):
      cd = True
    if method == 'preset' and playlist != None and target != None and cd == False:
      def check_playlist(playlist):
        with open('./playlists/playlist_info.json','r',encoding='utf-8') as f:
          metadata = json.load(f)
        mxp = metadata[playlist]
        return mxp
      mdata = check_playlist(playlist)
      song = TinyTag.get(f'./playlists/{playlist}/{target}')
      nex = str(datetime.timedelta(seconds=round(song.duration)))
      mdata = {"name": mdata["songs"][target]["name"], "icon": mdata["cover"], "length": nex, "volume": mdata["songs"][target]["volume"]}
      xdata = {"dmr": dmr, "method": method, "content": content, "playlist": playlist, "target": target, "cd": cd, "mdata": mdata}
    elif method == 'preset' and cd == True:
      content = content.split("?")
      playlist = content[1]
      target = content[2]
      def check_playlist(playlist):
        with open('./playlists/playlist_info.json','r',encoding='utf-8') as f:
          metadata = json.load(f)
        mxp = metadata[playlist]
        return mxp
      mdata = check_playlist(playlist)
      song = TinyTag.get(f'./playlists/{playlist}/{target}')
      nex = str(datetime.timedelta(seconds=round(song.duration)))
      mdata = {"name": mdata["songs"][target]["name"], "icon": mdata["cover"], "length": nex, "volume": mdata["songs"][target]["volume"]}
      xdata = {"dmr": dmr, "method": method, "content": content, "playlist": playlist, "target": target, "cd": cd, "mdata": mdata}
    elif method == 'preset' and playlist == None and target == None:
      song = TinyTag.get(f'./music/{content}')
      nex = str(datetime.timedelta(seconds=round(song.duration)))
      mdata = {"name": content, "icon": None, "length": nex, "volume": 0.5}
      xdata = {"dmr": dmr, "method": method, "content": content, "playlist": playlist, "target": target, "cd": cd, "mdata": mdata}
    elif method == 'url':
      if os.path.exists('./ky_song.mp3'):
        os.remove('./ky_song.mp3')
      if os.path.exists('./ky_stit.txt'):
        os.remove('./ky_stit.txt')
      if os.path.exists('./ky_stit.vtt'):
        os.remove('./ky_stit.vtt')
      if os.path.exists('./ky_thum.webp'):
        os.remove('./ky_thum.webp')
      if os.path.exists('./ky_thum.jpg'):
        os.remove('./ky_thum.jpg')
      if os.path.exists('./ky_thum.png'):
        os.remove('./ky_thum.png')
      ydl_opts = {
      'format': 'bestaudio/best',
      'quiet': True,
      'writesubtitles': True,
      'writethumbnail': True,
      'skip_download': True,
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
        }],
      }
      with YoutubeDL(ydl_opts) as ydl:
        ydl.download([content])
        info = ydl.extract_info(content, download=False)
      mdata = {"name": info["title"], "icon": info["thumbnail"], "length": nex, "volume": 0.5}
      xdata = {"dmr": dmr, "method": method, "content": content, "playlist": playlist, "target": target, "cd": cd, "mdata": mdata}
    else:
      return None
    return xdata
