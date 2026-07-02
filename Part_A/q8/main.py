from abc import ABC, abstractmethod

class Report(ABC):
    """Abstract base class for different types of reports."""

    def __init__(self):
        print("instance of report abstract class is created")

    @abstractmethod
    def generate_report(self):
        """Method to generate report (to be implemented in child classes)."""
        pass

class AttendanceReport(Report):
    """Generates attendance report for an intern."""

    def __init__(self, attendance, total_days):
        self.attendance = attendance
        self.total_days = total_days

    def generate_report(self):
        """Calculates and displays attendance percentage."""
        print("your attendance report:",(self.attendance/self.total_days)*100)

class PerformanceReport(Report):
    """Generates performance report for an intern."""

    def __init__(self, project_status, total_projects):
        self.project_status = project_status
        self.total_projects = total_projects

    def generate_report(self):
        """Calculates and displays performance percentage."""
        print("your performance report:",(self.project_status/self.total_projects)*100)

attendance_report_1 = AttendanceReport(80, 100)
attendance_report_1.generate_report()

performance_report_1 = PerformanceReport(3, 4)
performance_report_1.generate_report()