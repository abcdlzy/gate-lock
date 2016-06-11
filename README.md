# IC-gate-lock
hardware: Raspberry Pi , ACR122U and S50 Mifare1 (M1) card

using : sudo python card.py

需要安装树莓派RPi.GPIO,pyscard,web库

数据存放在 /card

##需要注意的坑
在ACR122U的使用中：  
可能需要屏蔽默认的驱动
```Bash  
blacklist pn533  
blacklist nfc  
```

应该需要安装
```Bash  
apt-get install libpcsclite1 pcsc-tools pcscd
```

安装web.py
```Bash
wget http://webpy.org/static/web.py-0.37.tar.gz  
tar xvfz web.py-0.37.tar.gz  
cd web.py-0.37  
sudo python setup.py install  
```

在card.py中，对于远程解锁的支持，如果是sudo开机运行，请写固定路径，例如webpage文件夹在/gate/webpage，那么，请把295行代码改为
```Python
render=web.template.render("/gate/webpage")
```
##部分功能原计划实现后发现不妥  
1:刷卡时更新密钥A和B（刷卡在读写临界点时会出现数据损坏情况）  
2:原计划刷卡后改变开关状态，后发现这样子不如直接刷卡后开10秒钟锁然后又自动对锁激活好

##效果
![image](https://github.com/abcdlzy/nothing/blob/master/2F55375B-F160-42F1-AA61-B327EB090D88.png)
![image](https://github.com/abcdlzy/nothing/blob/master/67BCBC6C-FB98-4A03-A4E6-77B7D726765E.png)


