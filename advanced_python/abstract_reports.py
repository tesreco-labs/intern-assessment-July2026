"""
Task 8: Abstract Class
========================
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Report(ABC):
    """Abstract base class for generating reports."""

    def __init__(self, title):
        self.title = title
        self.generated_at = None

    @abstractmethod
    def generate_report(self):
        """Generate the report. Must be implemented by subclasses."""
        pass

    def get_header(self):
        """Return a formatted report header."""
        return (
            f"{'=' * 55}\n"
            f"  TESRECO Technologies - {self.title}\n"
            f"  Generated: {self.generated_at or 'Not yet generated'}\n"
            f"{'=' * 55}"
        )


class AttendanceReport(Report):
    """Generates attendance reports for interns."""

    def __init__(self):
        super().__init__("Attendance Report")

    def generate_report(self, attendance_data=None):
        """
        Generate an attendance report.

        Args:
            attendance_data (list): List of dicts with intern_id, name, present, absent

        Returns:
            str: Formatted attendance report
        """
        self.generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not attendance_data:
            attendance_data = [
                {"intern_id": "TES001", "name": "Khushi", "present": 22, "absent": 3},
                {"intern_id": "TES002", "name": "Raushan", "present": 20, "absent": 5},
                {"intern_id": "TES003", "name": "Vaibhav", "present": 24, "absent": 1},
                {"intern_id": "TES004", "name": "Nidhika", "present": 23, "absent": 2},
            ]

        report = self.get_header() + "\n\n"
        report += f"  {'ID':<10}{'Name':<15}{'Present':<10}{'Absent':<10}{'%':<10}\n"
        report += f"  {'-' * 50}\n"

        for record in attendance_data:
            total = record['present'] + record['absent']
            pct = (record['present'] / total * 100) if total > 0 else 0
            report += (
                f"  {record['intern_id']:<10}{record['name']:<15}"
                f"{record['present']:<10}{record['absent']:<10}{pct:.1f}%\n"
            )

        report += f"\n  Total Interns: {len(attendance_data)}\n"
        report += "=" * 55
        return report


class PerformanceReport(Report):
    """Generates performance reports for interns."""

    def __init__(self):
        super().__init__("Performance Report")

    def generate_report(self, performance_data=None):
        """
        Generate a performance report.

        Args:
            performance_data (list): List of dicts with intern_id, name, scores

        Returns:
            str: Formatted performance report
        """
        self.generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not performance_data:
            performance_data = [
                {"intern_id": "TES001", "name": "Khushi", "scores": [78, 90, 65, 88, 95]},
                {"intern_id": "TES002", "name": "Raushan", "scores": [82, 76, 90, 85, 88]},
                {"intern_id": "TES003", "name": "Vaibhav", "scores": [95, 92, 88, 94, 96]},
                {"intern_id": "TES004", "name": "Nidhika", "scores": [70, 75, 68, 72, 80]},
            ]

        report = self.get_header() + "\n\n"
        report += f"  {'ID':<10}{'Name':<15}{'Avg':<10}{'Grade':<10}{'Status':<15}\n"
        report += f"  {'-' * 55}\n"

        for record in performance_data:
            avg = sum(record['scores']) / len(record['scores'])
            if avg >= 90:
                grade, status = "A+", "Outstanding"
            elif avg >= 80:
                grade, status = "A", "Excellent"
            elif avg >= 70:
                grade, status = "B", "Good"
            elif avg >= 60:
                grade, status = "C", "Average"
            else:
                grade, status = "D", "Needs Improvement"

            report += (
                f"  {record['intern_id']:<10}{record['name']:<15}"
                f"{avg:<10.1f}{grade:<10}{status:<15}\n"
            )

        report += f"\n  Total Interns Evaluated: {len(performance_data)}\n"
        report += "=" * 55
        return report


# --- Demonstration ---
if __name__ == "__main__":
    # Cannot instantiate abstract class
    try:
        r = Report("Test")
    except TypeError as e:
        print(f"Cannot instantiate abstract class: {e}\n")

    # Attendance Report
    att_report = AttendanceReport()
    print(att_report.generate_report())

    print()

    # Performance Report
    perf_report = PerformanceReport()
    print(perf_report.generate_report())
