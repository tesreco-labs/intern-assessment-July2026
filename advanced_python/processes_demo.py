import multiprocessing


def build_performance_report(intern):
    name, score = intern
    return f"Performance report generated for {name}: {score}"


def generate_reports_for_interns(interns):
    if not interns:
        return []

    process_count = min(len(interns), multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=process_count) as pool:
        return pool.map(build_performance_report, interns)
