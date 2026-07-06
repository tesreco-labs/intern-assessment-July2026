import multiprocessing

from advanced_python.certificates import certificate_generator
from advanced_python.copy_demo import demonstrate_copy_difference
from advanced_python.csv_handler import add_record, delete_record, search_record
from advanced_python.exceptions import validate_intern_data
from advanced_python.functional_analysis import analyze_scores
from advanced_python.id_iterator import InternIDIterator
from advanced_python.inheritance_demo import TESRECOMentor, get_mro
from advanced_python.intern import Intern
from advanced_python.logging_config import log_error, log_login_event, log_report_generation
from advanced_python.performance import calculate_performance_score
from advanced_python.processes_demo import generate_reports_for_interns
from advanced_python.reports import AttendanceReport, PerformanceReport
from advanced_python.sqlite_crud import (
    create_intern,
    create_mentor,
    init_db,
    read_interns,
    read_mentors,
)
from advanced_python.threads_demo import run_threads


def run_all_demos():
    print("1. Intern Class Design")
    intern = Intern("TES001", "Lucky", "lucky@example.com", "Python", 3)
    print(intern)

    print("\n2. Performance Calculator")
    print(calculate_performance_score(90, 85, 88))

    print("\n3. Custom Iterator")
    print(list(InternIDIterator(limit=3)))

    print("\n4. Generator Function")
    for certificate in certificate_generator(["Lucky", "Raushan"]):
        print(certificate)

    print("\n5. Exception Handling")
    try:
        validate_intern_data("Vaibhav", "Vaibhav@gmail.com", "Data Science", 3)
        print("Intern data is valid")
    except Exception as error:
        log_error(str(error))
        print(error)

    print("\n6. Shallow Copy vs Deep Copy")
    print(demonstrate_copy_difference())

    print("\n7. Multiple Inheritance")
    mentor = TESRECOMentor("Amit", "EMP001", "Flask")
    print(mentor.display())
    print("MRO:", get_mro())

    print("\n8. Abstract Class")
    print(AttendanceReport("Lucky", 24, 30).generate_report())
    print(PerformanceReport("Lucky", 89).generate_report())

    print("\n9. Lambda & Functional Programming")
    print(analyze_scores([78, 90, 65, 88, 95]))

    print("\n10. File Handling")
    add_record(
        {
            "intern_id": "TES001",
            "name": "Lucky",
            "email": "lucky@example.com",
            "domain": "Python",
            "duration": 3,
        }
    )
    print(search_record("TES001"))
    print("Deleted:", delete_record("TES001"))

    print("\n11. Multithreading")
    print(run_threads())

    print("\n12. Multiprocessing")
    print(generate_reports_for_interns([("Lucky", 89), ("Raushan", 91)]))

    print("\n13. Logging")
    log_login_event("admin")
    log_report_generation("PerformanceReport")
    print("Events stored in tesreco.log")

    print("\n14. SQLite Integration")
    init_db()
    create_intern("TES001", "Lucky", "lucky@example.com", "Python")
    create_mentor("M001", "Amit", "Flask")
    print(read_interns())
    print(read_mentors())

    print("\n15. Project Structure")
    print("TESRECO Intern Management Portal structure is available in the project root.")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_all_demos()
