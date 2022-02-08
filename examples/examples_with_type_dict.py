from copy import deepcopy

from maintain_ner_position import insert_content, insert_content_extend_entity, \
    insert_entity, insert_entity_extend_entity, delete_sub_content, delete_entity_with_idx


def my_print(content, entity_list):
    print(content)
    print("实体列表：")
    for e in entity_list:
        print("\t\t({type:{type_len}}, {start:{start_len}}, {end:{end_len}}, {value:{value_len}})".format(
            type=e["type"], type_len=max(len(e["type"]) for e in entity_list),
            start=e["start"], start_len=max(len(str(e["start"])) for e in entity_list),
            end=e["end"], end_len=max(len(str(e["end"])) for e in entity_list),
            value=e["value"], value_len=max(len(e["value"]) for e in entity_list),
        ))
    print()


def test_insert_content():
    content = "小明去招商银行。"
    entity_list = [
        {"type": "机构", "start": 3, "end": 7, "value": "招商银行"},
        {"type": "品牌", "start": 3, "end": 5, "value": "招商"},  # 支持重叠实体
    ]

    for i in range(len(content) + 1):  # 遍历所有情况测试
        print("insert_idx", i, insert_content(content, deepcopy(entity_list), i, "hello world"))


def test_insert_content_extend_entity():
    content = "小明去招商银行。"
    entity_list = [
        {"type": "机构", "start": 3, "end": 7, "value": "招商银行"},
        {"type": "品牌", "start": 3, "end": 5, "value": "招商"},  # 支持重叠实体
    ]
    for i in range(len(content) + 1):  # 遍历所有情况测试
        print("insert_idx", i, insert_content_extend_entity(content, deepcopy(entity_list), i, "hello world"))


def test_insert_entity():
    content = "小明去招商银行。"
    entity_list = [
        {"type": "机构", "start": 3, "end": 7, "value": "招商银行"},
        {"type": "品牌", "start": 3, "end": 5, "value": "招商"},  # 支持重叠实体
    ]
    content, entity_list = insert_content(content, entity_list, len(content) - 1, "对面的")
    content, entity_list = insert_entity(content, entity_list, len(content) - 1, "人民医院", insert_type="机构")
    my_print(content, entity_list)


def test_insert_entity_extend_entity():
    content = "小明去招商银行。"
    entity_list = [
        {"type": "机构", "start": 3, "end": 7, "value": "招商银行"},
        {"type": "品牌", "start": 3, "end": 5, "value": "招商"},  # 支持重叠实体
    ]
    my_print(*insert_entity_extend_entity(content, entity_list, 3, "中国", insert_type="国家"))


def test_compare_insert_entity():
    content = "小明去招商银行。"
    entity_list = [
        {"type": "机构", "start": 3, "end": 7, "value": "招商银行"},
        {"type": "品牌", "start": 3, "end": 5, "value": "招商"},  # 支持重叠实体
    ]
    print("原始文本和其实体列表：")
    my_print(content, entity_list)

    print("\n不扩展原实体：")
    my_print(*insert_entity(content, deepcopy(entity_list), 3, "中国", insert_type="国家"))

    print("\n扩展原实体：")
    my_print(*insert_entity_extend_entity(content, deepcopy(entity_list), 3, "中国", insert_type="国家"))


def test_delete_content():
    content = "小明去欧阳锋家。"
    entity_list = [
        {"type": "人名", "start": 3, "end": 6, "value": "欧阳锋"},
        {"type": "复姓", "start": 3, "end": 5, "value": "欧阳"},  # 支持重叠实体
    ]

    for i in range(len(content) + 1):
        for j in range(i + 1, len(content) + 1, 1):
            print("start", i, "end", j, delete_sub_content(content, deepcopy(entity_list), start=i, end=j))

    # 待删除待片段起止索引相同
    print("start", 3, "end", 3, delete_sub_content(content, deepcopy(entity_list), start=3, end=3))


def test_delete_entity_with_idx():
    content = "小明去欧阳锋家。"
    entity_list = [
        {"type": "人名", "start": 3, "end": 6, "value": "欧阳锋"},
        {"type": "复姓", "start": 3, "end": 5, "value": "欧阳"},  # 支持重叠实体
    ]

    for i in range(len(entity_list)):
        print(delete_entity_with_idx(content, deepcopy(entity_list), entity_idx=i))


def test_compare_delete():
    content = "小明去欧阳锋家。"
    entity_list = [
        {"type": "人名", "start": 3, "end": 6, "value": "欧阳锋"},
        {"type": "复姓", "start": 3, "end": 5, "value": "欧阳"},  # 支持重叠实体
    ]

    print("保留被删除掉一部分的实体：", delete_entity_with_idx(content, deepcopy(entity_list), 1))

    print("不保留被删除了一部分的实体：",
          delete_entity_with_idx(content, deepcopy(entity_list), 1, keep_sub_entity=False))


if __name__ == '__main__':
    # test_insert_content()
    # test_insert_content_extend_entity()
    # test_insert_entity()
    # test_insert_entity_extend_entity()
    # test_compare_insert_entity()
    # test_delete_content()
    # test_delete_entity_with_idx()
    test_compare_delete()
