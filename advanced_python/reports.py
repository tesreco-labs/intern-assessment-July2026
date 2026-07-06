from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def generate_report(self):
        pass


class AttendanceReport(Report):
    def __init__(self, intern_name, present_days, total_days):
        self.intern_name = intern_name
        self.present_days = present_days
        self.total_days = total_days

    def generate_report(self):
        percentage = (self.present_days / self.total_days) * 100
        return f"{self.intern_name} Attendance: {percentage:.2f}%"


class PerformanceReport(Report):
    def __init__(self, intern_name, score):
        self.intern_name = intern_name
        self.score = score

    def generate_report(self):
        return f"{self.intern_name} Performance Score: {self.score}"
