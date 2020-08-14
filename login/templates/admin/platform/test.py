from login.templates.admin.platform.common.operate_mysql import billing_select


def main():
    sum = 0  # 定义变量做累加器

    n = int(input('n='))  # 从键盘上输入累加的范围

    for x in range(n):
        sum += (x + 1)

    print(sum)


if __name__ == '__main__':
    main()

