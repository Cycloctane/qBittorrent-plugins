# qBittorrent-plugins

qbittorrent搜索插件。使用bt/pt站点的RSS接口进行搜索。

目前支持：
- mikan.py: Mikan Project (https://mikanime.tv)
- nexus.py: 使用NexusPHP且开启RSS功能的pt站点
- skyeysnow.py: 天雪论坛(pt)

## 使用方法

参考https://github.com/qbittorrent/search-plugins/wiki/Install-search-plugins

### Mikan Project

直接添加到qBittorrent搜索插件中。

qBittorrent -> 搜索 -> 搜索插件 -> 安装新插件 -> 输入以下链接：

https://raw.githubusercontent.com/Cycloctane/qBittorrent-plugins/master/engines/mikan.py

### NexusPHP

注意：通过RSS接口进行搜索的行为可能违反pt站点的使用规则，使用前请仔细查阅pt站点规则或咨询站点管理员。

1. 下载nexus.py到本地：https://raw.githubusercontent.com/Cycloctane/qBittorrent-plugins/master/engines/nexus.py
2. 将pt站url和passkey分别输入nexus.py的`SITE_URL`和`PASSKEY`。
3. 根据站点分类规则修改`CATAGORIES`(可选)。
4. 在 qBittorrent -> 搜索 -> 搜索插件 -> 安装新插件 中从本地文件添加编辑后的nexus.py

### 天雪

1. 下载skyeysnow.py到本地：https://raw.githubusercontent.com/Cycloctane/qBittorrent-plugins/master/engines/skyeysnow.py
2. 将passkey输入skyeysnow.py的`PASSKEY`。
3. 在 qBittorrent -> 搜索 -> 搜索插件 -> 安装新插件 中从本地文件添加编辑后的skyeysnow.py
