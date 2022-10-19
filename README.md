# autoXparty

## 程序用途

懂的人自然会用

## 使用简介

### 当前开发/测试环境

- Python 3.10.6
- Selenium 4.5.0
- webdriver-manager 3.8.3
- chrome 106.0.5249.119

基于Python 3 以及 Selenium 4 以上的版本运行应该没有问题。

### 安装依赖

1. 安装 `Python 3`

特别针对 `Windows` 用户，`Mac` 与 `Linux` 系统通常自带（若系统自带的Python为2.7，也许要安装Python3）

官方下载地址： https://www.python.org/downloads （当前最新版本为：3.10.8）

2. 安装 `Selenium` （当前版本 4.5.0）


```bash
$ pip install selenium
```

3. 安装Selenium辅助包 `webdriver-manager`

```bash
$ pip install webdriver-manager
```

4. 安装Chrome浏览器（俗称`谷歌浏览器`）

Windows平台，建议下载官方离线安装包： [👉 Win64 bit](https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B206B747B-D0A5-B2F9-0C1E-45DAC2AF249F%7D%26lang%3Den%26browser%3D3%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup64.exe)   或  [👉 Win32 bit](https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B206B747B-D0A5-B2F9-0C1E-45DAC2AF249F%7D%26lang%3Den%26browser%3D3%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dstable-arch_x86-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup.exe)

5. 下载当前程序包

点击下载： [👉 autoXparty main.zip](https://github.com/prgrmthkwc/autoXparty/archive/refs/heads/main.zip)

将下载的 `main.zip` 解压至某目录


## 运行程序

除了需要安装以上依赖程序以外，运行前还需要简单配置。

1. 简单配置

```bash
$ cd path/to/autoXparty/
$ cp xparty.cfg.example.json xparty.cfg.json
```

根据自身情况修改 xparty.cfg.json 配置文件。

当前需要修改 `username` 和 `url` 两项值，程序会读取它们。

2. 运行程序

```bash
$ python xparty.py
```



## 希望你喜欢！