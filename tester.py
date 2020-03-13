import sys
sys.path.append('./mod_pbxproj')

from pbxproj import XcodeProject

config = {
'xcodeproj': './cloud-search.xcodeproj'
}
# open project
project = XcodeProject.load(config['xcodeproj'] + '/project.pbxproj')

class GroupStruct:
    Dict = {} # if an object has parrent, then it's content is it's parent
    def __init__(self, project):
        self.groups = project.objects.get_objects_in_section('PBXGroup')

        # initialize the dictionary of groups
        for item in self.groups:
            itemID = item.get_id().upper()
            for child in item.children:
                self.Dict[child.upper()] = itemID


    def iterateFiles(self, file, maxIter = 100):
        curr = file
        list = []
        iter = 0
        while curr in self.Dict:
            parent = self.Dict[curr]
            list.append(parent)
            curr = parent
            iter += 1
            if iter > maxIter:
                return None

        return list

    def constructPath(self):
        pass

def addFileToHeader():
    pass

test = GroupStruct(project)

# print(test.Dict)