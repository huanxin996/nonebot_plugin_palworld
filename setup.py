import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_palworld",
    version="0.0.8",
    author="Huan Xin",
    author_email="mc.xiaolang@foxmail.com",
    description="幻兽帕鲁服务器rest api使用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huanxin996/nonebot_plugin_palworld",
    packages=setuptools.find_packages(),
    install_requires=['aiohttp>=3.11.11','nonebot2>=2.4.1','nonebot-adapter-onebot>=2.4.6'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)