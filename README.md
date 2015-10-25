# IC-gate-lock
hardware: Raspberry Pi , ACR122U and S50 Mifare1 (M1) card

using : sudo python card.py

需要安装树莓派RPi.GPIO,pyscard库

数据存放在 /card

##需要注意的坑
在ACR122U的使用中：  
可能需要屏蔽默认的驱动  
blacklist pn533  
blacklist nfc  
  
应该需要安装  
apt-get install libpcsclite1 pcsc-tools pcscd

##部分功能原计划实现后发现不妥  
1:刷卡时更新密钥A和B（刷卡在读写临界点时会出现数据顺坏情况）  
2:原计划刷卡后改变开关状态，后发现这样子不如直接刷卡后开10秒钟锁然后又自动对锁激活好




