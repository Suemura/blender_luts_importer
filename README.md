# blender_luts_importer
import&amp;apply luts to images!  
レンダリング画像に対してLUT(Look Up Table)を適用し、カラーグレーディングを行うアドオンです。 
<img width="1920" alt="サムネイル.png (1.4 MB)" src="https://img.esa.io/uploads/production/attachments/9489/2020/07/07/78640/28cf081a-087f-470f-861d-10023ca0cfb8.png">

# Attention
私はカラーコレクション等の技術者でなく、色情報の専門的知識は有りません。  
処理の工程で16bitのTIFF形式でLutを適用していますが、色情報の欠損などの問題がある場合があります。  
Photoshopによる結果の比較などを行った限り、大きな違いは見当たりませんでした。使用は自己責任でお願いします。  

# installation
現状のバージョンでは、各自でBlenderにColourパッケージをインストールしなければならない  
またこのとき、Blender2.83内蔵のPythonにインストールしなければならない  
  
`$ cd C:\Program Files\Blender Foundation\Blender 2.83\2.83\python\bin`  
`$ .\python.exe -m pip install colour-science`  
  

# How to use
処理はレンダー結果である、"Render Result"に対して行われる  
UV/ImageエディタのLUTタブで操作を行う  
Lutファイル(*.Cube)を設定する  
あとはApplyを押すことで、"img.tiff"がBlenderのImageにLut適用済みの画像として追加される  
