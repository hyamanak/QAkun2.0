import re

class PhraseObj(list):
     
     #for tag searches
     source_tag = "<source>"
     target_tag = "<target>"
     special_tag = "<memsource:tag "
     tag_id_str = ""
     seg_num = "<segment id="
     unit_tag = "<unit id="
     id_attr = "id="
     
     tags_to_check = ['literal', 'emphasis', 'link']
     
     sample_seg = '<source>"Pin" the RHEL version to 8.6 by using the <pc id="source1" dataRefStart="source1">subscription-manager release --set 8.x</pc> command.</source>'
 
     
     #Regex for tag attributes
     segment_num_reg = "<segment id=\"(.*?)\" "  ##ex. 10, 11, 12
     tag_id_reg = "<memsource:tag id=\"(.*?)\">" ## source1, source2, etc...
     tag_type_reg = "<memsource:type>(.*?)</memsource:type>" ##emphasis, literal, etc...
     source_reg = "<source>(.*?)</source>"
     target_reg = "<target>(.*?)</target>"
     in_segmenet_tag_reg = "<pc id=\"(.*?)\" dataRefStart=\"(.*?)\">" 
     seg_begin_reg = "memsource:tGroupBegin=\"(.*?)\""
     seg_end_reg = "memsource:tGroupEnd=\"(.*?)\""
     unit_id_reg = "<unit id=\"(.*?)\""
     btw_sp_tag_texts = r'<pc id=\"{}\" (.*?)>(.*?)</pc>'
     tag_exists = "<pc id=(.*?)>(.*?)</pc>"

     def __init__(self, unit_list) -> None:
          self.unit_info = self.get_unit_info(unit_list) ##

          self.__segment_nums =  self.get_tag_element(unit_list, self.seg_num) ##list ['<segment id="155" state="final">']
          self.segment_num_list = self.get_segment_num(self.__segment_nums) ##[155]
          
          self.__source = self.get_tag_element(unit_list, self.source_tag) ##<source>...</source> list
          self.__target = self.get_tag_element(unit_list, self.target_tag) ##<target>...</target> list
          
          self.segment_source = self.set_segment(self.__source) ##{10: '', 11: ''}
          self.segment_target = self.set_segment(self.__target) ##{10: '', 11: ''}

          self.sp_segment = self.get_tag_element(unit_list, self.special_tag) ##get <memsource:tag id list, can be multiple 
          self.tag_exists_in_unit = self.if_tag_exists_in_unit() #True or False       
          
          self.tag_ids_types = self.get_tag_ids_types(self.sp_segment) ##list, literal, emphasis and etc {source1:literal, source2:emphasis} etc
          
          self.content = self.get_tag_with_content(self.__source, 0)
          #self.tag_set_list = self.get_tag_set_list(self.__source)
          self.converted = self.convert_tags2original(self.__source[0])
          
          ##TODO handle single tag
          
          #self.tag_set_list_target = self.get_tag_with_content(0)
          #['<pc id="source3" dataRefStart="source3">false</pc>', ...]
          
          #self.the_number_of_segments = self.get_the_numbers_of_segment(self.unit_info)
          
          #self.stripped_source = self.__strip_segment_tag(self.segment_source, self.source_reg)
          #self.stripped_target = self.__strip_segment_tag(self.segment_target, self.target_reg)
          
          #self.complete_unit_info = self.get_complete_unit_info()
          
          #self.tag_id = self.__get_tag_ids(self.get_tag_with_content(0))
     
     def get_source(self):
          return self.__source[0]
     def get_target(self):
          return self.__target
     
     def __get_tag_ids(self, tag_set_list) -> dict:
          #takes single str with tag <pc id="source3" dataRefStart="source3">false</pc>
          #returns [source3, source2...]
          return [re.search(self.in_segmenet_tag_reg, tag_set).group(1) for tag_set in tag_set_list]
     
     def if_tag_exists_in_unit(self):
          return len(self.sp_segment) != 0
     
     def if_tag_exists_in_seg(self, segment):
          return bool(re.search(r"<pc id=(.*?)>(.*?)</pc>", segment))
     
     def get_tag_set_list(self, segment) -> list:
          return [segment for seg in segment if self.if_tag_exists_in_seg(segment)]
     
     def get_seg_with_tag(self, segment):
          return [seg for seg in segment if self.if_tag_exists_in_seg(seg)]
          
                    
     def get_tag_with_content(self, segment, group) -> list:
          #segment = takes SINGLE source or target segment, takes 'souce' or 'target'
          #takes tag_ids_types {source1:literald, source2:emphasis}
          #returns: following
          #group 0: ['<pc id="source3" dataRefStart="source3">false</pc>',...]
          #group 1: ['dataRefStart="source3"', 'dataRefStart="source1"', 'dataRefStart="source2"']
          #group 2: ['false', 'visible', 'caCMCUserCert']
          #if there is none, return given segment
          
          segment = self.get_seg_with_tag(segment)
          #print(segment)
          ids = [id for id in self.tag_ids_types.keys()]
          #r'<pc id=\"{}\" (.*?)>(.*?)</pc>'
          content = {id:re.search(self.btw_sp_tag_texts.format(id), seg).group(group) for id in ids for seg in segment}
          return content if len(content) != 0 else segment
     
     def id2tag(self, tag, btw_txt):
          return "<" + tag + ">" + btw_txt +"</" + tag + ">"
          
     
     def convert_tags2original(self, segment) -> str:
          btw_txt = self.get_btw_txt(segment)
          #print(btw_txt)
          for key, value in self.content.items():
               tag = self.id2tag(self.tag_ids_types[key], btw_txt)
               #print(tag)
               segment = segment.replace(value, tag)
          return segment
               
          
     def get_btw_txt(self, tag_set):
          ##returns in-between texts <pc id="source1">subscription-manager release --set 8.x</pc> --> subscription-manager release --set 8.x
          return re.search(r"<pc id=(.*?)>(.*?)</pc>", tag_set).group(2)
     
     def get_complete_unit_info(self) -> dict:
          result = self.unit_info
          result['source'] = self.stripped_source
          result['target'] = self.stripped_target
          return result
     
     def __strip_segment_tag(self, seg, tag_reg) -> dict:
          #takes segemnt list and remove tag and return list {156: 'Prepare the RootCA to sign other CMC certificate requests'}
          return {key:re.findall(tag_reg, value)[0] for key, value in seg.items()}
     
     def set_actual_tag(self, segment) -> str:
          ##takes single segment (self.segment_source or segment_target to return str (segment replaced xliff tag with actual tag)
          open_tag = '<pc id="{}" dataRefStart="{}">'.format(id)
          return re.findall(self.in_segmenet_tag_reg, segment)

# In addition, also change the <pc id="source1" dataRefStart="source1">visible</pc> parameter for the 
# <pc id="source2" dataRefStart="source2">caCMCUserCert</pc> profile to <pc id="source3" dataRefStart="source3">false</pc>:</source>

     def get_tag_element(self, list, tag) -> list:
          elements = [item for item in list if tag in item]
          return elements
      
     def set_segment(self, seg) -> dict: #set segment with seg_num {10: '', 11:''} '' is source or target, removes source, target tag
          num_list = self.segment_num_list
          return {key:value for key, value in zip(num_list, seg)}
          
     def get_the_numbers_of_segment(self, unit_info) -> int:
          return self.unit_info['seg_end'] - self.unit_info['seg_begin'] + 1
          
     def get_unit_info(self, unit_list) -> dict:
          #returns {id: num, begi_segn:num, end_seg: num}
          #<unit id="123" memsource:tGroupBegin="155" memsource:tGroupEnd="155">
          unit_info = {
               'id': 0, 
               'seg_begin': 0, 
               'seg_end': 0,
               }

          unit_seg = self.get_tag_element(unit_list, self.unit_tag) ##['<unit id="123" memsource:tGroupBegin="155" memsource:tGroupEnd="155">']
          regex_items = [self.unit_id_reg, self.seg_begin_reg, self.seg_end_reg]
          
          if len(unit_seg) != 1:
               raise ValueError("multiple units exist...")
          else:
               unit_seg = unit_seg[0] #'<unit id="123" memsource:tGroupBegin="155" memsource:tGroupEnd="155">'
               return {
                    unit_key:int(self.get_tag_attributes(
                         regex_item, unit_seg)[0]
                                 ) for regex_item, unit_key in zip(regex_items, unit_info.keys())
                    } 
               
     def get_tag_attributes(self, regex, segment) -> list:
          ##get tag attribute values
          return re.findall(regex, segment)

     def get_segment_num(self, seg_num_seg) -> list:
          ## takes a segment of segment number list [10, 11, 12] to return 
          nums_str = ''.join(seg_num_seg)
          num_str_list = re.findall(self.segment_num_reg, nums_str)
          return  [int (num) for num in num_str_list] #return int list, instead of str
          
     def get_tag_ids_types(self, sp_list) -> dict: ##{source1:literal, source2:emphasis}
          sp_tag_list_str = ''.join(sp_list)
          
          tag_ids = self.get_tag_attributes(self.tag_id_reg, sp_tag_list_str)
          tag_types = self.get_tag_attributes(self.tag_type_reg, sp_tag_list_str)
          
          return {key:value for key, value in zip(tag_ids, tag_types)}
          
     