# 主要部分
# 首先我们要从caselist.txt文件中读取需要执行的case名称，然后将他们添加到python自带的unittest测试集中，
# 最后执行run()函数，执行测试集
import os
import unittest
from common.HTMLTestRunner import HTMLTestRunner
import readConfig as readConfig
from common.Log import MyLog as MyLog
from common.configEmail import Email


log = MyLog.get_log()
logger = log.get_logger()


class RunAll:
    # 根据caselist.txt内容，找到需要执行的test_case
    def __init__(self):
        self.email = Email
    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    # 将test_case添加到test_suite中
    def set_case_suite(self):
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_model = []

        for case in self.caseList:
            case_file = os.path.join(readConfig.proDir, "testCase")
            print(case_file)
            case_name = case.split("/")[-1]
            print(case_name+".py")
            discover = unittest.defaultTestLoader.discover(case_file, pattern=case_name + '.py', top_level_dir=None)
            suite_model.append(discover)

        if len(suite_model) > 0:
            for suite in suite_model:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    # 使用HTMLTestRunner执行test_suite
    def run(self, result=None):
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("********TEST START********")

                # resultPath = os.path.join(proDir, "result")
                # logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))

                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            # send test report by email
            if int(on_off) == 0:
                self.email.send_email()
            elif int(on_off) == 1:
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    run = RunAll()
    run.run()

