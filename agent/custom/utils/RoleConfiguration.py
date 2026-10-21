"""
崩坏3角色配置。

attack_template 为空时不会参与自动识别；仍可通过“自动战斗-星环角色选择”
手动指定。后续补截图时，把图片放到 resource/base/image/自动战斗索引/角色名.png，
再把 attack_template 改成对应相对路径即可进入自动识别。
"""

ROLE_CONFIG = {
    "真理之律者": {
        "cls_name": "HerrscherOfTruth",
        "metadata": {"DMG": "ice", "type": "mecha", "weight": 2},
        "template": ["自动战斗识别/真理之律者.png"],
        "attack_template": "自动战斗索引/真理之律者.png",
    },
    "梅比乌斯": {
        "cls_name": "Meibiwusi",
        "metadata": {"DMG": "lightning", "type": "mecha", "weight": 2},
        "template": ["自动战斗识别/梅比乌斯.png"],
        "attack_template": "自动战斗索引/梅比乌斯/普攻.png",
    },
    "爱愿妖精": {
        "cls_name": "LoveElf",
        "metadata": {"DMG": "ice", "type": "sd", "weight": 2},
        "template": ["自动战斗识别/爱愿妖精.png"],
        "attack_template": "自动战斗索引/爱愿妖精.png",
    },
    "崩落符": {
        "cls_name": "FengHuangOfVicissitude",
        "metadata": {"DMG": "fire", "type": "bio", "weight": 2},
        "template": ["自动战斗识别/崩落符.png"],
        "attack_template": "自动战斗索引/崩落符.png",
    },
    "深空定锚·曙光": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "lightning", "type": "sd", "ring": "世界之星", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "女武神·巡矢": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "lightning", "type": "bio", "ring": "世界之星", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "女武神·重击": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "fire", "type": "mecha", "ring": "世界之星", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "享乐狂宴·邀影": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "ice", "type": "mecha", "ring": "命运之轮", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "破弃弧光·逐影": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "fire", "type": "psy", "ring": "命运之轮", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "瞒天乐游·曙影": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "physical", "type": "sd", "ring": "天衍之杯", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "孑遗千星": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "lightning", "type": "mecha", "ring": "无存之仪", "weight": 3},
        "template": ["自动战斗识别/孑遗千星.png"],
        "attack_template": "自动战斗索引/孑遗千星.png",
    },
    "诡戏千役[友情出演！]": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "fire", "type": "qua", "ring": "命运之轮", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "嗨♪爱愿妖精♪": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "ice", "type": "sd", "ring": "天衍之杯", "weight": 3},
        "template": ["自动战斗识别/爱愿妖精.png"],
        "attack_template": "自动战斗索引/爱愿妖精.png",
    },
    "咚！炽愿吉星": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "fire", "type": "sd", "ring": "升变之理", "weight": 3},
        "template": ["自动战斗识别/炽愿吉星.png"],
        "attack_template": "自动战斗索引/炽愿吉星.png",
    },
    "一客逍游": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "physical", "type": "bio", "ring": "命运之轮", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "位面武器·失序时空": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "lightning", "type": "mecha", "ring": "世界之星", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "逆命魔龙·降临！": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "fire", "type": "qua", "ring": "命运之轮", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "窈窕谍影": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "physical", "type": "img", "ring": "命运之轮", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "镇×偃月叩晓": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "physical", "type": "mecha", "ring": "天衍之杯", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "次生银翼": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "ice", "type": "mecha", "ring": "世界之星", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "药菀谜影": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "lightning", "type": "bio", "ring": "世界之星", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "天光驰彻": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "physical", "type": "img", "ring": "天衍之杯", "weight": 2},
        "template": [],
        "attack_template": "",
    },
    "天命难逃": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "fire", "type": "sd", "ring": "天衍之杯", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "浮生·渡尘之羽": {
        "cls_name": "FengHuangOfVicissitude",
        "metadata": {"DMG": "fire", "type": "bio", "weight": 2},
        "template": ["自动战斗识别/崩落符.png"],
        "attack_template": "自动战斗索引/崩落符.png",
    },
    "月下誓约·予爱以心": {
        "cls_name": "AstralRingFight",
        "metadata": {"DMG": "lightning", "type": "sd", "ring": "命运之轮", "weight": 3},
        "template": [],
        "attack_template": "",
    },
    "炽愿吉星": {
        "cls_name": "FieryWishingStar",
        "metadata": {"DMG": "fire", "type": "sd", "weight": 2},
        "template": ["自动战斗识别/炽愿吉星.png"],
        "attack_template": "自动战斗索引/炽愿吉星.png",
    },
}
