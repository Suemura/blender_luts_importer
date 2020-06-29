# blender_luts_importer
import&amp;apply luts to images!  

# installation
現状のバージョンでは、各自でBlenderにColourパッケージをインストールしなければならない  
またこのとき、Blender2.83内蔵のPythonにインストールしなければならない  
  
`$ cd C:\Program Files\Blender Foundation\Blender 2.83\2.83\python\bin`  
`$ .\python.exe -m pip install colour-science`  
  

# How to use
処理はレンダー結果である、"Render Result"に対して行われる  
UV/ImageエディタのLUTタブで操作を行う  
Lutファイル(*.Cube)を設定する  
あとはApplyを押すことで、"img.tiff"がBlenderのImageにLut適用済みの画像が追加される  
