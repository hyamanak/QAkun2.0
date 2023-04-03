from MxliffObj import MxliffObj

with open('test.mxliff', encoding='utf-8') as mxliff, open('output.thml', 'a+') as  html:

    ##get a block
    mxliff_group_open= "<group id="
    mxliff_group_close = "</group>"
    storing = False
    block = []

    for line in mxliff: ##block []
        if mxliff_group_open in line:
            storing = True
        
        if mxliff_group_close in line:
            block.append(mxliff_group_close)
            storing = False
            #print(block)
            group = MxliffObj(block)
            if group.tag_info != None:
                print(group.tag_info)
                print(group.segment_num)
                print('<p>source: ' + group.source_with_tags +'</p>')
                print('<p>target: ' + group.target_with_tags +'</p>')
                
            else:
                print(group.segment_num)
                print('source: ' + group.source)
                print('target: ' + group.target)
            block = [] ##resetting obj

        if storing:
            block.append(line.strip("\n"))