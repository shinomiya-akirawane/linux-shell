import unittest

from src.appFactory import AppFactory


class TestAppFactory(unittest.TestCase):
    def testAppFactory(self):
        appNames = [
            "cat",
            "cd",
            "cut",
            "echo",
            "find",
            "grep",
            "head",
            "ls",
            "pwd",
            "sort",
            "tail",
            "uniq",
            "wc"
        ]

        appFunctions = [
            "<class 'apps.cat.Cat'>",
            "<class 'apps.cd.Cd'>",
            "<class 'apps.cut.Cut'>",
            "<class 'apps.echo.Echo'>",
            "<class 'apps.find.Find'>",
            "<class 'apps.grep.Grep'>",
            "<class 'apps.head.Head'>",
            "<class 'apps.ls.Ls'>",
            "<class 'apps.myPwd.Pwd'>",
            "<class 'apps.sort.Sort'>",
            "<class 'apps.tail.Tail'>",
            "<class 'apps.uniq.Uniq'>",
            "<class 'apps.wc.Wc'>"
        ]

        appCombination = zip(appNames, appFunctions)

        for name, function in appCombination:
            appInstance = AppFactory.create(name)
            self.assertEqual(str(type(appInstance)), function)

    def testUnsafeFactory(self):
        unsafeAppNames = [
            "_cat",
            "_cd",
            "_cut",
            "_echo",
            "_find",
            "_grep",
            "_head",
            "_ls",
            "_pwd",
            "_sort",
            "_tail",
            "_uniq",
            "_wc"
        ]
        for unsafeAppName in unsafeAppNames:
            unsafeApp = AppFactory.create(unsafeAppName)
            self.assertEqual(
                str(type(unsafeApp)),
                "<class 'apps.decorator.UnsafeDecorator'>",
            )

    def testAppNotFind(self):
        with self.assertRaises(RuntimeError):
            AppFactory.create("fakeApp")


if __name__ == "__main__":
    unittest.main()
