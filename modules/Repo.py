# class Repo with 6 attributes: index, project_id, project_name, subproject_locator, number_of_bugs, bug_ids

class Repo:
    def __init__(self, index, project_id, project_name, subproject_locator, number_of_bugs, bug_ids):
        self.index = index
        self.project_id = project_id
        self.project_name = project_name
        self.subproject_locator = subproject_locator
        self.number_of_bugs = number_of_bugs
        self.bug_ids = bug_ids

    def __str__(self):
        return 'index: {}, project_id: {}, project_name: {}, subproject_locator: {}, number_of_bugs: {}, bug_ids: {}'.format(self.index, self.project_id, self.project_name, self.subproject_locator, self.number_of_bugs, self.bug_ids)