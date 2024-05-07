from datetime import datetime

def get_timestamp():
    return str(round(datetime.now().timestamp()))

class testCount:

    def __init__(self, title:str, total_tests:int):
        self.tested_count= 0
        self.passed_count= 0
        self.failed_count= 0
        self.title= title
        self.total_tests= total_tests

    def add_count(self):
        self.tested_count += 1

    def passed(self):
        self.passed_count += 1
        
    def failed(self):
        self.failed_count += 1

    def get_tested(self):
        return self.tested_count

    def get_passed(self):
        return self.passed_count

    def get_failed(self):
        return self.failed_count
    
    def get_stats(self):
        return f"{self.title}\nTotal number of tests: {self.total_tests}\nTotal test ran: {self.tested_count}\nPassed: {self.passed_count}\nFailed: {self.failed_count}\n"
    
    



