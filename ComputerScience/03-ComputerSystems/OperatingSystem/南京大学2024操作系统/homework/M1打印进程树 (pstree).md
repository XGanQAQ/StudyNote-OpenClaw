# 打印进程树

## 目标
做一个简单的进程树，打印出进程的树状结构。

## 怎么做？
- 了解进程相关的API
- 获得进程编号
- 遍历所有进程
- 建树打印
- 检测结果

## 进程相关API
如何通过c程序获得ubuntu系统进程信息。  

所有的进程信息都存储在/proc文件内
/proc/<进程号>/statue 存储了父类信息

## 处理逻辑
按进程号顺序获得进程信息，得到此的pid。再设置一个数组，往后遍历statue中的父类进程信息，如果相符则为其子类，递归遍历，直到该进程没有子类则停止

Linux操作系统的进程以树形结构管理，很自然的，我就可以使用递归的形式来遍历进程信息。
首先找到跟进程，父进程为0的进程，再递归查询，输出，就能得到进程树

## C语言文件读取相关知识 
[[文件读取]]
[[文件夹读取]]
[[字符串处理]]
## 源代码

```c
#include <stdio.h>

#include <assert.h>

#include <stdlib.h>

#include <string.h>

#include <dirent.h>

#include <ctype.h>

  

#define PROC_DIR "/proc"

  

// 清除字符数组中的Tab字符

void clear_Tab_char_array(char* array) {

    char *write_array = array;

    while (*array) {

        if (*array != '\t') {

            *write_array = *array;

            write_array++;

        }

        array++;

    }

    *write_array = '\0';

}

  

// 获取某进程的父进程ID

void get_parent_pid(char* pid, char* p_pid) {

    char filename[256];

    snprintf(filename, sizeof(filename), "/proc/%s/status", pid);  // 构造文件路径

  

    FILE *file = fopen(filename, "r");  // 打开文件

    if (file == NULL) {

        perror("fopen-get-ppid");

        return;  // 打开文件失败

    }

  

    char line[256];

  

    // 逐行读取文件

    while (fgets(line, sizeof(line), file)) {

        // 查找 "PPid" 行

        if (strncmp(line, "PPid:", 5) == 0) {

            // 解析出父进程的PID

            sscanf(line, "PPid:\t%s", p_pid);

            break;

        }

    }

  

    fclose(file);  // 关闭文件

}

  

// 获取某进程的进程名称

void get_name_pid(char* pid, char* name) {

    char filename[256];

    snprintf(filename, sizeof(filename), "/proc/%s/status", pid);  // 构造文件路径

  

    FILE *file = fopen(filename, "r");  // 打开文件

    if (file == NULL) {

        perror("fopen-get-pName");

        return;  // 打开文件失败

    }

  

    char line[256];

  

    // 逐行读取文件

    while (fgets(line, sizeof(line), file)) {

        // 查找 "Name" 行

        if (strncmp(line, "Name:", 5) == 0) {

            // 解析出进程名称

            sscanf(line, "Name:\t%s", name);

            break;

        }

    }

  

    fclose(file);  // 关闭文件

}

  

// 打印所有以id为父类的进程

void print_child_processes(char* id, int level) {

    DIR *dir = opendir(PROC_DIR);  // 打开/proc目录

    if (dir == NULL) {

        perror("opendir");

        return;

    }

  

    struct dirent *entry;

    while ((entry = readdir(dir)) != NULL) {

        if (isdigit(entry->d_name[0])) {  // 过滤掉非进程的目录

            char pid[256];

            char p_name[256];

            char p_pid[256];

  

            strcpy(pid, entry->d_name);

            get_parent_pid(pid, p_pid);

  

            // 如果此进程的父进程ID等于传入的id

            if (strcmp(p_pid, id) == 0) {

                get_name_pid(pid, p_name);  // 获取进程名称

                for (int i = 0; i < level; i++) {

                    printf("    ");

                }

                printf("(%s)%s\n", pid, p_name);  // 打印进程信息

                print_child_processes(pid, level + 1);  // 递归查找子进程

            }

        }

    }

  

    closedir(dir);  // 关闭目录

}

  

// 打印命令行参数

void printArg(int argc, char *argv[]) {

    for (int i = 0; i < argc; i++) {

        assert(argv[i]);

        printf("argv[%d] = %s\n", i, argv[i]);

    }

    assert(!argv[argc]);

}

  

int main(int argc, char *argv[]) {

    //printArg(argc, argv);  // 打印命令行参数

    print_child_processes("0",0); // 打印进程树

  

    return 0;

}


```

## 其他知识笔记
assert的作用
int main(int argc,char *argv[])中参数的作用
使用makefile 优化测试，自动化构建
