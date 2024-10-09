
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
repo_to_url = get_variables('main_variables.json', 'repo_to_url')


for xml_file in xml_files:
    dict_elements = {}
    warnings = []
    filename = xml_file.split('/')[-1].split('.')[0]
    file, warnings = openXMLFile(xml_file, warnings)
    url_value, warnings = getXMLElement(file, 'url', warnings)       
    if not url_value:
        continue
    try:
        type_value, warnings = getXMLElement(file, 'type', warnings)  
        dict_elements.update({'type':type_value})
    except:
        pass
    for element in asset_elements:
        value, warnings = getXMLElement(file, element, warnings)
        dict_elements.update({element:value})
    dict_elements.update({'repo_name': repo_to_url[xml_file.split("/")[1]]})
    GlobalUpdates(filename, dict_elements, warnings)

for json_file in json_files:
    dict_elements = {}
    warnings = []
    filename = json_file.split('/')[-1].split('.')[0]
    file, warnings = openJSONFile(json_file, warnings)
    url_value, warnings = getJSONElement(file, 'url', warnings)
    if not url_value:
        continue
    try:
        type_value, warnings = getJSONElement(file, 'type', warnings)  
        dict_elements.update({'type':type_value})
    except:
        pass
    for element in asset_elements:
        value, warnings = getJSONElement(file, element, warnings) 
        dict_elements.update({element:value})
    dict_elements.update({'repo_name': repo_to_url[json_file.split("/")[1]]})
    GlobalUpdates(filename, dict_elements, warnings)

for key, value in global_warnings.items():
    printWarnings(value, key)

print("Files ignored:")
for f in global_ignore:
    print(f"\t{f}")
    
'''Sort assets into seperate dictionaries'''
codesystems = {}
conceptmaps = {}
capabilitystatements = {}
valuesets = {}
profiles = {}
extensions = {}
for asset, elements in global_elements.items():
    for k,v in elements.items():
        if k=='url':
            if 'codesystem' in v.lower():
                codesystems.update({asset:elements})
            elif 'conceptmap' in v.lower():
                conceptmaps.update({asset:elements})
            elif 'capabilitystatement' in v.lower():
                capabilitystatements.update({asset:elements})
            elif 'valueset' in v.lower():
                valuesets.update({asset:elements})
            else:
                profiles.update({asset:elements})
for asset in profiles.keys():
    if asset['type'] == 'extension':
        extensions.update(profile[asset])
        profile.pop(asset)
        
codesystems = dict(sorted(codesystems.items()))
valuesets = dict(sorted(valuesets.items()))
profiles = dict(sorted(profiles.items()))
conceptmaps = dict(sorted(conceptmaps.items()))
capabilitystatements = dict(sorted(capabilitystatements.items()))

'''Create markdown file'''
def code_assets(asset,elements, title):
    #print(f"<tr>\n  <td>{str(asset)}</td>\n", file = md_file)
    if title == 'ValueSet' or title == 'CodeSystem':
        print(f'''<td><a href="{elements['repo_name']}/{title}-{elements['id']}">{elements['id']}</a></td>\n''',file=md_file)
    else:
        print(f'''<td><a href="{elements['repo_name']}/{elements['id']}">{elements['id']}</a></td>\n''',file=md_file)
    elements.pop('url')
    elements.pop('repo_name')
    elements.pop('id')
    for element,value in elements.items():
        print(f"  <td> {str(value)} </td>\n", file = md_file)
        #md_file.write('''<td>''')
        #md_file.write(str(value))
        #md_file.write('''</td>''')
    print(f"</tr>\n", file = md_file)
    #md_file.write('''\n</tr>\n''')
    

def write_section(md_file, title, items):
    print(f"## {title}s\n<br>\n<table>", file=md_file)
    for asset, elements in items.items():
        code_assets(asset, elements, title)
    print(f"</table>\n<br><br>\n\n---\n\n",file=md_file)

path = './guides/Interoperability-Standard-Registry-Guide/About-Interoperability/FHIR-Assets/R4-Assets.page.md'

if os.path.exists(path):
    os.remove(path)
md_file = open(path,"w")

write_section(md_file, "Profile", profiles)
write_section(md_file, "Extension", extensions)
write_section(md_file, "ValueSet", valuesets)
write_section(md_file, "CodeSystem", codesystems)
write_section(md_file, "ConceptMap", conceptmaps)
write_section(md_file, "CapabilityStatement", capabilitystatements)

md_file.close()




