# texas-holdem-tools
A series Tools for texas hold'em with python. 

# Install

```python
    # install requirement
    git clone https://github.com/DarainS/texas-holdem-tools
    cd ./texas-holdem-tools
    pip3 install -r requirement.txt
```
```python
    # install mongodb
    # by Docker
    docker pull mongo
    and then mongo.py file would auto run mongodb by docker.
```

## Include

1. 牌力计算算法

2. 胜率计算器：蒙特卡洛随机与regular两种方式。

3. 牌力收敛功能。将169种牌的胜率不断收敛。



## Improve

1. 直接计算7张牌的牌力，相较于5张性能提高了30~40倍。

## Todo

- [x] 建立翻后result模型，数据格式为{level0:1,name0:高牌,num0:10,winNum0:6,rate0:0.1,winRate0:0.6,...}

- [ ] 如何较好的计算一手牌的翻前强度。
- [ ] 计算对手的range范围
- [ ] 面对对手的range范围的胜率
