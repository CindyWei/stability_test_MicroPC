# 常见问题
**Q：python中文字符比较？**
A：str == u‘中文’

**Q：import子文件夹中的py类？**
A：在子文件中新建一个"__init__.py"的文件，包装成python package，在需要调用的py文件中，**from** subfoldername.pyclass **import** *