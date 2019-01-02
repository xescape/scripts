'''
Created on Jun 28, 2016
@author: javi
'''
import re

'''
Takes path
Returns (header, body) as separated lines
No further modifications
'''

def readTable(filepath):
    with open(filepath, 'r') as input:
        raw_text = input.read()
    
    line_split = re.split('\n', raw_text)
    header = line_split[0]
    body = line_split[1:-1]
    
    return header, body
        
'''
requires the table tuple (header, body) from readTable
returns the modified tuple in the same format
'''
def reverseOrder(table):        
    header, body = table
    
    grad_pattern = '(?<=colorlist=\"\")(.+?)(?=\")'
    val_pattern = '(?<=\")([0-9\.]+?[|].+?)(?=\")'
    results = []
    
    for line in body:
        grad = re.search(grad_pattern, line).group(1)
        vals = re.search(val_pattern, line).group(1)
        grad_list = re.split(',', grad)
        val_list = re.split('\|', vals)
        
        grad_list.reverse()
        val_list.reverse()
        
        new_grad = ','.join(grad_list)
        new_val = '|'.join(val_list)
        
        #sub the old strings with the new ones.
        mod_line = re.sub(grad_pattern, new_grad, line)
        mod_line2 = re.sub(val_pattern, new_val, mod_line)
        
        results.append(mod_line2)
    
    return (header, results)

def changeColor(input_path, color_dict):
    
    def colrep(matchobj):
        return color_dict[matchobj.group(0)]
    
    with open(input_path, 'r') as input:
        data = input.read()
    
    for color in color_dict:
        data = re.sub(color, colrep, data)
    
    return data
        
##helpers


if __name__ == '__main__':

#     ## To Reverse Order
#     directory = '/data/new/javi/reshape'
#     file_name = 'plasmo_partial.csv'
#     output_name = 'rev_plasmo_partial.csv'
#     
#     directory = '/data/new/javi/toxo/SNPSort80/matrix/cytoscape'
#     file_name = 'new_table.csv'
#     output_name = 'new_table2.csv'
# 
#     path = '/'.join([directory, file_name])
#     output_path = '/'.join([directory, output_name])
#      
#     with open(output_path, 'w') as output:
#         header, body = reverseOrder(readTable(path))
#         output.write('\n'.join([header] + body))
        
    ## To change color
    directory = '/d/data'
    file_name = 'type2nodes_2.csv'
    output_name = 'type2nodes_3.csv'
      
    path = '/'.join([directory, file_name])
    output_path = '/'.join([directory, output_name])
      
#     color_dict = {'#AA3F00' : '#E31A1C', #blue
#                   '#AAFE55' : '#FDBF6F', #red
#                   '#FED455' : '#FF7F00', #green
#                   '#006AAA' : '#CAB2D6', #orange
#                   '#00AA6A' : '#A6CEE3',
#                   '#AA003F' : '#1F78B4',
#                   '#15AA00' : '#B2DF8A',
#                   '#9400AA' : '#33A02C',
#                   '#94AA00' : '#FB9A99',}
      
#     color_dict = {'#E31A1C' : '#E41A1C', #blue
#                   '#FDBF6F' : '#377EB8', #red
#                   '#FF7F00' : '#4DAF4A', #green
#                   '#CAB2D6' : '#984EA3', #orange
#                   '#A6CEE3' : '#FF7F00',
#                   '#1F78B4' : '#FFFF33',
#                   '#B2DF8A' : '#A65628',
#                   '#33A02C' : '#F781BF',
#                   '#FB9A99' : '#00FFF3',}
    
    color_dict = {'#FF00BF' : '#FF9933',
                  '#00FEFF' : '#FF0000'}
    
    with open(output_path, 'w') as output:
        output.write(changeColor(path, color_dict))
    
    print('Table changed.')
