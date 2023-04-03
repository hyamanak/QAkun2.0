import re

class QaEngine():
    extra_space_cri_list = ['^ +.{2}',
                             '､ ', ' ､',
                             '｡ ', ' ｡',
                             '\( +', ' +\)',
                             '[ぁ-ゖァ-ヴー] +[ぁ-ゖァ-ヴー]',
                             ': $']
    
    missing_space_cri_list = [
          '[A-Za-z0-9:?!|%$#\)][ぁ-んァ-ンー-龥]',
          '[ぁ-んァ-ンー-龥][A-Za-z0-9?!%$#|\(]',
    ]
    
    zenkaku_non_jp_chars = '[Ａ-Ｚａ-ｚ０-９：！？＋＊＾％＄＃＠；／｛｝［］（）　]'

    zenkaku_special = '[＞＜＆’”]'
    zenkaku_special_dict = {'＞':'&gt;', '＜':'&lt;', '＆':'&amp;', "’":'&apos;', '”':'&quot;'}

    jp_parenthesis = '[「」『』]'

    segment_status = None

    cho_on_issue_list = None
    
    non_translatables = ['&lt;literal&gt;']
    punctuation = r"jp_char.$"

    def __init__(self, source, target, tag_info):
        self.source = source
        self.target = target
        self.tag_info = tag_info
        
        
        
        
        ##space issues
        if self.has_issue_from_list(self.extra_space_cri_list):
            self.report
        
        ##tag space issues
        
        ##punctuation issues
        
        
        #brackets
        if self.has_issue(self.jp_parenthesis):
            
        #whole_width
            
        ##non_translatables
        
        ##numbers
        
        ##spelling
    '''
    tag_info
    (
        {0: {'id': '3', 'type': 'literal', 'content': '&lt;literal&gt;'},
        1: {'id': '4', 'type': 'emphasis', 'content': '&lt;emphasis&gt;'}
        }, 
        {0: {'id': '3', 'type': 'literal', 'content': '&lt;literal&gt;'}, 
        1: {'id': '4', 'type': 'emphasis', 'content': '&lt;emphasis&gt;'}
        }
    )
    '''
    ##literal content has to be equal
    ##for emphasis only, if both source and target only contain half-width char, then it has to be equal
    ##method checker (camel, pascal, snake_case)
    
    #句読点 ､^ abc abc^､｡    
    def error_check(self) -> str:
        ##print out the all the issues report
        self.has_issues()
        pass
    
    def has_issue(self, regex):
        return bool(re.search(regex, self.target))
    
    def has_issue_from_list(self, regex_list):
        return any(self.has_issue(regex) for regex in regex_list)
    
    def get_issue_list(self, regex):
        return re.findall(regex, self.target)

    def 
    
    def has_bf_af_tag_space_issues(self) -> bool:
        #space no space between chars  and tags, (Ex. xxx<literal>aaa</literal>aaa)
        regex = r"\S<(.*?)>|<(.*?)>\S"
        return self.has_issues(regex)

    def has_tag_colon_space_issues(self) -> bool:
        #sapce between tag and colon </literal>^: (this should not exist)
        regex = r'&gt; +:'
        return self.has_issues(regex)
    
    
    
    def has_tag_content_issues():
        pass
    
    def has_spelling_issues(self) -> bool:
        #checks english spelling in target if any
        for item in self.non_translatables:
            if item in self.target.:
            
    
    def has_numbering_issues(self) -> bool:
        pass
    
    def has_non_translatable_translated(self) -> bool:
        pass
    
    def get_plain_text(self, target):
        pass
    
    def get_space_error_list(self, target) -> list:
        return re.findall(self.zen_han, target) + re.findall(self.han_zen, target)
    
    def get_jp_parenthesis(self) -> list:
        pass

    def get_spelling_issues(self):
        pass

    def check_numbers(source, target):
        pass

    def get_numbers(self):
        pass

    def check_literal(source, target, tag):
        pass

    def get_literal(source, target, tag):
        pass

    def set_tags(source, target, tags):
        pass