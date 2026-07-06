import copy


def demonstrate_copy_difference():
    intern_projects = [
        {
            "intern": "Khushi",
            "projects": ["Attendance Module", "Performance Report"],
        }
    ]
    shallow_copy = copy.copy(intern_projects)
    deep_copy = copy.deepcopy(intern_projects)

    intern_projects[0]["projects"].append("Certificate Generator")

    return {
        "original": intern_projects,
        "shallow_copy": shallow_copy,
        "deep_copy": deep_copy,
    }
