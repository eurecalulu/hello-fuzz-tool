# hellofuzzing-instrument

使用 JavaParser 对 fuzz target 进行程序转换，在每个分支处插装覆盖率信息代码，运行插装后的代码可以通过输出流的方式查看此次运行分支覆盖情况。

## 环境

jdk8  maven

## 使用方法

```
mvn clean package
java -jar .\target\hellofuzzing-instrument-1.0-SNAPSHOT.jar "path/to/the/target"
```

运行结果是会在target目录下生成一个新的 java 文件，名字是在原来java文件的基础上添加“HelloFuzzing”。

插装后的代码运行时的覆盖率信息通过输出流最后一行的二进制字符串查看，01的个数就是分支数，0代表未覆盖，1代表覆盖。