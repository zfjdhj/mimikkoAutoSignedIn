# mimikko_api_test

用于兽耳桌面相关接口测试

## 使用

1. 抓包软件获取登录时的app_id,Authorization

2. 创建action secrets
`secrets.APP_ID`,`secrets.AUTHORIZATION`;

    **可选功能**：日志输出到文件，需要设定`secrets.SECRET_TOKEN`

3. 修改config.json

    ``` json
    {
        "code": "ruri",
        "app_version": "3.1.7",
        "max_favorability": 135950,
        "servant_list": [
            "nemuri",
            "momona",
            "miruku2"
        ]
    }
    ```

    参数含义：
    | 参数 | 含义 |
    | :- | :- |
    | code | 需要操作的助手名称，具体参考下文 |
    | app_version | 当前app版本，暂时无影响 |
    | max_favorability | 好感上限阈值 |
    | servant_list | 助手列表 |

    支持的助手code：
    | 助手名称 | code |
    | :-: | :-: |
    | 魔女日记 | nononabook |
    | 诺诺纳 | nonona |
    | 梦梦奈 | momona |
    | 爱莉安娜 | ariana |
    | 米璐库 | miruku |
    | 奈姆利 | nemuri |
    | 琉璃 | ruri |
    | 阿尔法零 | alpha0 |
    | 米露可 | miruku2 |
    | 优莉卡 | ulrica |

4. 可选功能：

    4.1. 日志输出到文件，取消注释`auto_sign_in.yml`中`name:push_log`相关内容

    如不需要，请注释掉

    4.2 每日图片输出到文件，消息推送等等，没有这些功能，未来也不会做，与现有[插件版](https://github.com/zfjdhj/zfjbot-mimikko)功能重合。

## Hoshino插件版

项目地址<https://github.com/zfjdhj/zfjbot-mimikko>

## 说明

这只是一个脚本，不要期望有太多功能。

或者使用大佬的另一版本

<https://github.com/cyb233/mimikkoAutoSignIn>

## 更新

### 20210521

1. 新增功能：当助手好感达到`好感上限阈值`，自动切换至`助手列表`下一助手

### 远古更新

1. 新增日志输出到文件，需要设定secrets.SECRET_TOKEN

    **注意**: 脚本包含上传功能，已关闭action push触发，如有需要请自行开启（会套娃），待测试完毕后尽快关闭

2. 新增config.json用于设定助手

3. 感谢cyb233大佬提供的建议
