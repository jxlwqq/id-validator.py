

**中华人民共和国居民身份证**、**中华人民共和国港澳居民居住证**以及**中华人民共和国台湾居民居住证**号码验证工具（Python 版）支持 15 位与 18 位号码。

## 其他语言版本

[PHP 版本](https://github.com/jxlwqq/id-validator)


## 安装

 

## 使用

> `440308199901101512` 和 `610104620927690` 示例大陆居民身份证均为随机生成的假数据，如撞车，请联系删除。
> `810000199408230021` 和 `830000199201300022` 示例港澳台居民居住证为北京市公安局公布的居住证样式号码。

### 验证身份证号合法性

验证身份证号是否合法，合法返回 `True`，不合法返回 `False`：

 

### 获取身份证号信息

当身份证号合法时，返回分析信息（地区、出生日期、星座、生肖、性别、校验位），不合法返回 `False`：
 

返回信息格式如下：

```python
{
'addressCode'   : '440308',          # 地址码   
'abandoned'     : 0,                 # 地址码是否废弃，1 为废弃的，0 为正在使用的
'address'       : '广东省深圳市盐田区', # 地址
'birthdayCode'  : '1999-01-10',      # 出生日期
'constellation' : '水瓶座',           # 星座
'chineseZodiac' : '卯兔',             # 生肖
'sex'           : 1,                 # 性别，1 为男性，0 为女性
'length'        : 18,                # 号码长度
'checkBit'      : '2'                # 校验码
}
```

> 注：判断地址码是否废弃的依据是[中华人民共和国行政区划代码历史数据集](https://github.com/jxlwqq/address-code-of-china)，本数据集的采集源来自：[中华人民共和国民政部](http://www.mca.gov.cn/article/sj/xzqh//1980/)，每年更新一次。本数据集采用 csv 格式存储，方便大家进行数据分析或者开发其他语言的版本。

### 生成可通过校验的假数据
伪造符合校验的身份证：
 

## 参考资料

* [中华人民共和国公民身份号码](https://zh.wikipedia.org/wiki/中华人民共和国公民身份号码)

* [中华人民共和国民政部：行政区划代码](http://www.mca.gov.cn/article/sj/xzqh/)

* [中华人民共和国行政区划代码历史数据集](https://github.com/jxlwqq/address-code-of-china)

* [国务院办公厅关于印发《港澳台居民居住证申领发放办法》的通知](http://www.gov.cn/zhengce/content/2018-08/19/content_5314865.htm)

* [港澳台居民居住证](https://zh.wikipedia.org/wiki/港澳台居民居住证)

## Change Log


## License
[MIT](LICENSE)


