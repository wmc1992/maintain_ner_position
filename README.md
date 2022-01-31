# maintain_ner_position

在做实体抽取相关的任务时，在做预处理、后处理等工作时经常会遇到需要对原始文本做增删改。同时还想要保证对原始文本增删改之后，其对应的实体列表中各个实体起止索引能够同步做更新。

本项目提供几个简单的对原始文本做增删改的函数，同时能够维护其实体列表中的各索引同步修改。

## 使用说明

### 数据结构

实体支持两种数据结构：`dict` 和 `tuple`；

#### `dict` 类型

每个实体为一个字典时，包含四个字段：

* `start`：该实体的起始索引，索引值遵循左闭右开规则；
* `end`：该实体的终止索引，索引值遵循左闭右开规则；
* `type`：该实体的类型；
* `value`：该实体的值；

举例如下：

```python
content = "小明去欧阳锋家。"
entity_list = [
    {"type": "人名", "start": 3, "end": 6, "value": "欧阳锋"},
    {"type": "复姓", "start": 3, "end": 5, "value": "欧阳"}  # 支持重叠实体
]
```

#### `tuple` 类型

每个实体为tuple类型时，也要包含上述四部分信息，其顺序为：`(start, end, type, value)`；

举例如下：

```python
content = "小明去欧阳锋家。"
entity_list = [(3, 6, "人名", "欧阳锋"), (3, 5, "复姓", "欧阳")]  # 支持重叠实体
```

> 推荐使用 `dict` 类型，代码内部实际上是先将 `tuple` 类型转为 `dict` 类型，然后进行逻辑处理，逻辑处理完成后再转换回去。

### 快速使用

#### 插入文本

插入文本的功能如下面的代码示例。可以调用函数 `insert_content` 只插入一段文本；也可以调用函数 `insert_entity` 插入一个新实体，此时需要传入新实体的实体类型。

关于**旧实体的扩展**：如下面的例子所示，"招商银行"是一个实体，如果在文本"小明去招商银行。"的索引 `3` 位置插入新文本："中国"，由于新插入的文本与实体"招商银行"紧邻，那么实体"招商银行"可以保持不变，也扩展为"中国招商银行"。调用函数 `insert_xxx` 时不会对旧实体做扩展，调用函数 `insert_xxx_extend_entity` 时会对旧实体做扩展。

```python
from maintain_ner_position import insert_content, insert_content_extend_entity

content = "小明去招商银行。"
entity_list = [
    {"type": "机构", "start": 3, "end": 7, "value": "招商银行"},
    {"type": "品牌", "start": 3, "end": 5, "value": "招商"},  # 支持重叠实体
]

print("不扩展实体：")
print(insert_content(content, deepcopy(entity_list), 3, "中国"))

print("\n扩展实体：")
print(insert_content_extend_entity(content, deepcopy(entity_list), 3, "中国"))

print("\n插入的文本作为一个新实体，旧实体不做扩展：")
print(insert_entity(content, deepcopy(entity_list), 3, "中国", insert_type="国家"))

print("\n插入的文本作为一个新实体，旧实体做扩展：")
print(insert_entity_extend_entity(content, deepcopy(entity_list), 3, "中国", insert_type="国家"))
```

输出：

```
不扩展实体：
('小明去中国招商银行。', [{'type': '机构', 'start': 5, 'end': 9, 'value': '招商银行'},
                      {'type': '品牌', 'start': 5, 'end': 7, 'value': '招商'}])

扩展实体：
('小明去中国招商银行。', [{'type': '机构', 'start': 3, 'end': 9, 'value': '中国招商银行'},
                      {'type': '品牌', 'start': 3, 'end': 7, 'value': '中国招商'}])

插入的文本作为一个新实体，旧实体不做扩展：
('小明去中国招商银行。', [{'type': '机构', 'start': 5, 'end': 9, 'value': '招商银行'},
                       {'type': '品牌', 'start': 5, 'end': 7, 'value': '招商'},
                       {'type': '国家', 'start': 3, 'end': 5, 'value': '中国'}])

插入的文本作为一个新实体，旧实体做扩展：
('小明去中国招商银行。', [{'type': '机构', 'start': 3, 'end': 9, 'value': '中国招商银行'},
                      {'type': '品牌', 'start': 3, 'end': 7, 'value': '中国招商'},
                      {'type': '国家', 'start': 3, 'end': 5, 'value': '中国'}])
```

> 说明：实际执行时，会直接在原实体列表上进行修改，如果不希望修改原始实体列表，则需要使用 deepcopy()；如果可以在原实体列表上进行修改，则不需要使用 deepcopy()；

#### 删除文本

删除文本的功能如下面的代码示例。可以调用函数 `delete_content` 直接删除一段指定的文本；也可以调用函数 `delete_entity_with_idx` 删除一个指定实体对应的文本。

当一个实体被删除掉了一部分之后，该实体是否保留，可由参数 `keep_sub_entity` 控制。比如下例中的"招商银行"，被删除掉了最后的那个"行"字之后，如果想保留"招商银"作为实体，可将参数 `keep_sub_entity` 设置为 `True`，如果不想保留可将该参数设置为 `False`。

```python
from maintain_ner_position import delete_sub_content, delete_entity_with_idx

content = "小明去招商银行。"
entity_list = [
    {"type": "机构", "start": 3, "end": 7, "value": "招商银行"},
    {"type": "品牌", "start": 3, "end": 5, "value": "招商"},  # 支持重叠实体
]

print("删除文本：\n",
      delete_content(content, deepcopy(entity_list), start=6, end=7, keep_sub_entity=True))

print("删除文本，丢弃所有被删除了一部分的实体：\n",
      delete_content(content, deepcopy(entity_list), start=5, end=7, keep_sub_entity=False))

print("删除指定实体对应的文本：\n",
      delete_entity_with_idx(content, deepcopy(entity_list), entity_idx=1, keep_sub_entity=True))

print("删除指定实体对应的文本，丢弃所有被删除了一部分的实体：\n",
      delete_entity_with_idx(content, deepcopy(entity_list), entity_idx=1, keep_sub_entity=False))
```

输出：

```
删除文本：
 ('小明去招商银。', [{'type': '机构', 'start': 3, 'end': 6, 'value': '招商银'},
                  {'type': '品牌', 'start': 3, 'end': 5, 'value': '招商'}])

删除文本，丢弃所有被删除了一部分的实体：
 ('小明去招商。', [{'type': '品牌', 'start': 3, 'end': 5, 'value': '招商'}])

删除指定实体对应的文本：
 ('小明去银行。', [{'type': '机构', 'start': 3, 'end': 5, 'value': '银行'}])

删除指定实体对应的文本，丢弃所有被删除了一部分的实体：
 ('小明去银行。', [])
```

### 其他使用说明

所有索引在使用时遵循左闭右开原则。

## License

[MIT License](./LICENSE)
