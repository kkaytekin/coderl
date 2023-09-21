import data_crawler

query = '?c=Programming+Language+%3A%3A+Python+%3A%3A+3&c=Programming+Language+%3A%3A+Python+%3A%3A+3+%3A%3A+Only&c=Topic+%3A%3A+Scientific%2FEngineering+%3A%3A+Artificial+Intelligence&o=&q='

repos = data_crawler.get_all_repos(query)

# for repo in repos:
# Do stuff with the repo
    