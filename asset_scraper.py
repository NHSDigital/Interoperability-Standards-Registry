
import xml.etree.ElementTree as ET
import json
import os


def openXMLFile(xml_file,warnings):        
    try:
        tree = ET.parse(xml_file)
    except Exception as e:
        warnings.append("\t\tThe code has an error that needs to be fixed before it can be checked: "+str(e))
        return {}, warnings
    root = tree.getroot()
    return root,warnings


def openJSONFile(file, warnings):
    try:
        with open(file, 'r') as j:
            jsonFile = json.loads(j.read())
    except Exception as e:
        print("\t\tThe code has an error that needs to be fixed before it can be checked:"+ str(e))       
        return {}, warnings
    return jsonFile, warnings


def getXMLElement(xml_file, element, warnings):
    try:
        return xml_file.findall('./{*}'+element)[0].get('value'), warnings
    except:
        warnings.append("\t\t"+element+" - This element is missing")
        return "", warnings


def getJSONElement(jsonFile, element, warnings):
    try:
        return jsonFile[element], warnings
    except:
        warnings.append("\t\t"+element+" - This element is missing")
    return '',warnings


def printWarnings(warnings, file):
    if warnings:
        print("\t",file)
        for x in warnings:
            print(x)


def list_files(folder):
    ''' gather a list of xml & json files within a folder. Returns xml_files, json_files '''
    xml_files = []
    json_files = []

    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.xml'):
                xml_files.append(os.path.join(dirpath, filename))
            elif filename.endswith('.json'):
                json_files.append(os.path.join(dirpath, filename))
    return xml_files, json_files


def GlobalUpdates(filename, dict_elements, warnings):
    global_elements.update({filename:dict_elements})
    global_warnings.update({filename:warnings})

        
def get_variables(file, attribute):
    warnings = []
    open_file, warnings = openJSONFile(file, warnings)
    global_warnings.update({file:warnings})
    list, warnings = getJSONElement(open_file, attribute, warnings)
    global_warnings.update({str(file)+':'+str(list):warnings})
    return list
    
global_warnings = {}
global_elements = {}
global_ignore = []

xml_files, json_files = list_files('.')
asset_elements = get_variables('main_variables.json', 'asset_elements')
print(f"json files:{json_files}")


for xml_file in xml_files:
    dict_elements = {}
    warnings = []
    filename = xml_file.split('/')[-1].split('.')[0]
    file, warnings = openXMLFile(xml_file, warnings)
    for element in asset_elements:
        value, warnings = getXMLElement(file, element, warnings)
        if element == 'url' and not value:
            global_ignore.append(filename)
            continue        
        dict_elements.update({element:value})
    GlobalUpdates(filename, dict_elements, warnings)

for json_file in json_files:
    dict_elements = {}
    warnings = []
    filename = json_file.split('/')[-1].split('.')[0]
    file, warnings = openJSONFile(json_file, warnings)
    for element in asset_elements:
        value, warnings = getJSONElement(file, element, warnings)
        if element == 'url' and not value:
            global_ignore.append(filename)
            continue       
        dict_elements.update({element:value})
    GlobalUpdates(filename, dict_elements, warnings)

print(f"global_elements:{global_elements}")
for key, value in global_warnings.items():
    printWarnings(value, key)

print("Files ignored:")
for f in global_ignore:
    print(f"\t{f}")
    

if os.path.exists("asset.md"):
    os.remove("asset.md")
md_file = open(f"asset.md","w")
md_file.write('''
## TEST
<br>
<table>
''')


for asset, elements in global_elements.items():
    md_file.write('''<tr>
    <td>''')
    md_file.write(str(asset)) 
    md_file.write('''</td>''')
    for element,value in elements.items():
        md_file.write('''<td>''')
        md_file.write(str(value))
        md_file.write('''</td>''')
    md_file.write('''\n</tr>\n''')
md_file.close()


for asset, elements in global_elements.items():
    print(elements)
    for k,v in elements.items():
        print(v)





