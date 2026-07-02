# Original list of intern projects
intern_project = ["news-aggregator", "realtime-chat-app", "url-shortener", "expense-tracker"]

print("original intern_project list",intern_project)

# Creating a copy of the list
deep_copy_intern_project = intern_project.copy()
deep_copy_intern_project[0] = "nextjs-doc-ai"

print("After copying the list:")
print(intern_project)
print(deep_copy_intern_project)

print("original intern_project list",intern_project)

# Creating a reference to the same list (shallow/reference copy)
shallow_copy_intern_project = intern_project
shallow_copy_intern_project[0] = "nextjs-doc-ai"

print("After assigning the same reference:")
print(intern_project)
print(shallow_copy_intern_project)