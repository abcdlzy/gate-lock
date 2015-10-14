# IC-gate-lock
hardware: Raspberry Pi , ACR122U and S50 Mifare1 (M1) card

using : sudo python card.py

需要安装树莓派RPi.GPIO,pyscard库

数据存放在 /card

在ACR122U的使用中：
可能需要屏蔽默认的驱动
blacklist pn533
blacklist nfc
需要安装
apt-get install libpcsclite1 pcsc-tools pcscd

部分功能在考虑到卡质量问题的情况下，未做实现：
1:刷卡时更新密钥A和B




