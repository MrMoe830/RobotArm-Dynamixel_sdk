# _**Robotics-Arm**_

--------------

简单的机械臂知识，希望对您有所帮助


 注意这是python文件，且代码主要用到机器人工具箱和其相关的依赖库，因此，如果您想在本地成功运行代码，您首先需要搭建好python环境并且安装[roboticstoolbox-python](https://github.com/petercorke/robotics-toolbox-python)

--------------

## 相关说明

- roboticstoolbox版本： 0.11.0

- python环境： anaconda3

- python虚拟环境： python3.9 

- 此中代码均以在上述配置下通过测试


--------------

## 安装



- python环境搭建
        
     - 您可以使用conda环境，并用它创建一个单独的robot环境用于您的项目
     
     - 您也可以直接使用python通过pip安装，这并不会对roboticstoolbox的使用有丝毫影响

       建议您使用conda环境，这也是目前python编程的主流环境，其具有强大的包管理功能，并且它允许您创建特定python版本的编程环境
       ( 即便您指定的是已经停止维护的python2环境 )。相关conda基础命令行使用方法见本栏底部“补充说明”部分。

- 下载anaconda

     - 您可以点击[此处](https://www.anaconda.com/)，它将带您一起跳转到anaconda官网进行下载
     
     - 您也可以点击[这里](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)，通过清华镜像站进行下载安装
     
       如果您担心下载速度过慢，那么建议您可以选择通过清华镜像站等国内站点进行下载，这将很大程度上提升您的下载速度。

- 注意事项
        
     - 在下载前，请注意您的系统类别，目前，anaconda支持 [Windows / macOS / Linux 版本](https://www.anaconda.com/products/distribution#Downloads)


><details><summary>补充说明</summary>
><p>
>conda创建新环境：
>        
> ```
>conda create -n <env_name> [python=<version>]
>```
>
>conda安装命令：
>
> ```
>conda install <pkg_name>
>```
>
>激活conda环境：
>
> ```
>conda activate <env_name>
>```
>
>退出当前conda环境：
>
> ```
>conda deactivate
>```
>
>删除conda环境：
>
> ```
>conda remove -n <env_name> --all
>```
>
>您进入环境后可以正常运行各种命令
>
</details></p>

#### 安装指令：

```
pip install roboticstoolbox-python
```

---------------
        

## 工具包安装报错怎么办？
    



这里，我仅针对安装过程中项目组遇到的最常见的由安装工具箱依赖项引发的报错提供一种解决办法：
 

场景描述如下：
 
  如果您使用的是Windows系统，且在使用pip命令安装机器人工具包的过程中遇到个别依赖项安装失败的报错，不要急，您可以先尝试以下方案。
        
    1. 查看本地编译环境
            
       您可以先查看您的本地C/C++的编译环境，在工具包的众多依赖项当中，有一些包为了提高运行效率，其底层采用的是C/C++语言编写，    
       因此，这就将导致其对您的本地C/C++编译环境有所要求。若您的C/C++编译组件过于滞后，您将无法正确解析或编译处理来自这些依赖包底层的一些请求。
        
    2. 安装符合要求的软件
 
       如果您符合上述情况，建议您可以安装Visual Studio 2019或更高版本，并在安装过程中勾选C++模块，
       这将帮助您解决由于C/C++环境问题而引起的安装报错。
        
    3. 提问与分享
 
       如果上述解决方案对您的报错不起作用，也请您不要气馁，您可以认真解读系统提示您的报错信息，或是将其复制到浏览器中查询解决方案，
       另外，我也同样欢迎您随时在Github上发布您的问题，我非常希望可以和您共同探讨，提供我力所能及的帮助。
       当然，如果您发现或顺利解决了一些额外的报错问题，我也强烈建议您把它拿出来分享，这将会对后人有非常大的帮助，并能很大程度上增加报错本身的意义。

最后，如果您觉得此中代码和信息对您有帮助，您可以关注我，或点亮您的星星，这将方便您在后期发布信息和查看本仓库的状态。
 
-------------
 
## 与我联系

个人Email:3247524712@qq.com

:blush: :blush: :blush:
