import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
]

setuptools.setup(
    name="maintain_ner_position",
    version="0.0.2",
    license="MIT",
    description="本项目提供几个简单的对原始文本做增删改的函数，同时能够维护其实体列表中的各索引同步修改。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wmc1992/maintain_ner_position",
    author="wmc1992",
    author_email="m18810541081@163.com",
    keywords="NER 索引",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.6",
)
