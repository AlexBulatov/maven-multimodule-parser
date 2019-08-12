import xml.etree.ElementTree as et
import sys
import json

allModules = dict()

def getDependencies(path):
    key = path.rsplit('\\', 1)[-1]
    allModules[key] = {'modules':list(), 'dependencies':list()}
    file = open( 'infos\\'+path.replace('\\', '-') + '.txt', 'w')
    tree = et.parse('C:\\projects\\'+path+'\\pom.xml')
    root = tree.getroot()

    modules = []
    dependencies = []

    for child in root:
        if child.tag[35:]=='modules':
            for subchild in child:
                modules.append(subchild)
                allModules[key]['modules'].append(subchild.text)
        if child.tag[35:]=='dependencyManagement':
            depChild = child[0]
            for subchild in depChild:
                dependencies.append(subchild)
                #allModules[key]['dependencies'].append(subchild[0].text+' '+subchild[1].text)
                if subchild[0].text == 'com.peterservice.rtco.com' :
                    allModules[key]['dependencies'].append(subchild[1].text)
        if child.tag[35:]=='dependencies':
            for subchild in child:
                dependencies.append(subchild)
                if subchild[0].text == 'com.peterservice.rtco.com' :
                    allModules[key]['dependencies'].append(subchild[1].text)

    file.write('---'+path+'---\n')
    file.write('MODULES:'+'\n')
    for i in modules:
        file.write(i.text+'\n')
    file.write('--------------------'+'\n')
    file.write('DEPENDENCIES:'+'\n')
    for i in dependencies:
        for ch in i:
            file.write(ch.text+ ' ')
        file.write('\n')
    for module in modules:
        getDependencies(path+'\\'+module.text)

def graphviz():
    res = "digraph G {\n"
    #Nodes
    for key in allModules.keys():
        res += key.replace("-", '_') + " [label= \""+key+"\"];\n"

    #Modules
    for key in allModules.keys():
        curNode = key.replace("-", '_')
        for mod in allModules[key]["modules"]:
            res+=curNode + " -> " + mod.replace("-", '_') + " [color=\"blue\"];\n"
        for dep in allModules[key]["dependencies"]:
            res+=curNode + " -> " + dep.replace("-", '_') + " [color=\"red\" overlap=scale];\n"
    res+= "}"
    return res;
    

tailored = 'cloud_deploy\\tailored_crm_b2b_rt_hq'
cam = 'cam'

chosenPath = tailored

getDependencies(chosenPath)
with open('infos\\'+chosenPath.rsplit('\\', 1)[-1] + '.json', 'w') as file:
    json.dump(allModules, file)

with open('infos\\'+chosenPath.rsplit('\\', 1)[-1] + '.gv', 'w') as file:
    file.write(graphviz())

#print(graphviz())
    


