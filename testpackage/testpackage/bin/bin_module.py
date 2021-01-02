from testpackage.lib import lib_module

def bin_print():
    print("this is from bin module.")
    lib_module.lib_print("hello world")
    print("after install local, I changed code")

if __name__ == '__main__':
    bin_print()
