import re
from urllib import request
from urllib import error


class Mooc:
    urlInit = 'https://mooc1.chaoxing.com/course/{{courseId}}.html'
    urlK = 'https://mooc1.chaoxing.com/nodedetailcontroller/visitnodedetail?courseId={{courseId}}&knowledgeId={{knowledgeId}}'
    workUrl = 'https://mooc1.chaoxing.com/api/selectWorkQuestion?workId={{workId}}&ut=null&classId=0&courseId={{courseId}}&utenc=null'

    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3'
    }

    def __returnWorkUrl(self, courseId, workId):
        url = self.workUrl.replace('{{courseId}}', courseId).replace(
            '{{workId}}', workId)
        return url

    def __getRequest(self, url):
        req = request.Request(url, headers=Mooc.headers)
        try:
            page = request.urlopen(req).read()
            page = page.decode('utf-8')
            return page
        except error.URLError as e:
            print('courseId可能不存在哦！', e.reason)
            exit()

    def __getFristData(self, courseId):
        # 组装初始URL，获取第一个包含knowledge
        url = self.urlInit.replace('{{courseId}}', courseId)

        htmls = self.__getRequest(url)

        # <a class="wh nodeItem"  href="?courseId=200080607&knowledgeId=102433017" data="102433017">
        #re_rule = 'courseId='+courseId+'&knowledgeId=(.*)">'

# <div id="" class="ml20 mb5  bgf3  mr10" data="102432997">
# <div id="courseChapterSelected" class="ml20 bbe pl0 bg1e mr10" data="102433017" rel="">

        re_rule = 'courseId='+courseId+'&knowledgeId=(.*)">'
        url_frist = re.findall(re_rule, htmls)

        if len(url_frist) > 0:
            return url_frist[0]
        else:
            print('courseId错误！')

    def __returnTitle(self, courseId, knowledgeId):
        url = self.urlK.replace('{{courseId}}', courseId).replace(
            '{{knowledgeId}}', knowledgeId)
        htmls = self.__getRequest(url)

        re_rule = '&quot;:&quot;work-(.*?)&quot;'
        wordId = re.findall(re_rule, htmls)
        wordId = list(set(wordId))  # 先转集合，再转队列  去重复

        title = []
        for x in wordId:
            wordUrl = self.__returnWorkUrl(courseId, x)
            html_work = self.__getRequest(wordUrl)
            title_rule = '<div class="Zy_TItle clearfix">\s*<i class="fl">.*</i>\s*<div class=".*">(.*?)</div>'
            title = title + re.findall(title_rule, html_work)
      
# <div id="" class="ml20 mb5  bgf3  mr10" data="102432997">
# <div id="courseChapterSelected" class="ml20 bbe pl0 bg1e mr10" data="102433017" rel="">

        #re_rule = '<a class=".*"  href="\?courseId=' + courseId+'&knowledgeId=.*" data="(.*)">'
        # re_rule = '<div id="(courseChapterSelected)?" class="[\s\S]*?" data="(\d*)">?'
        re_rule = '<div id="c?o?u?r?s?e?C?h?a?p?t?e?r?S?e?l?e?c?t?e?d?" class="[\s\S]*?" data="(\d*)">?'
        datas = re.findall(re_rule, htmls)

        return(title, datas)

    def getTextByCourseId(self, courseId):
        data_now = self.__getFristData(courseId)  # 第一个data需要再单独的一个链接里获取
        j = 1
        while data_now:
            listR = self.__returnTitle(courseId, data_now)

            title = listR[0]
            data = listR[1]

            for i, x in enumerate(data):
                if data_now == x:
                    if len(data) > (i+1):
                        data_now = data[i+1]
                    else:
                        data_now = None
                        print('获取题目结束.')

                    break

            # 打印题目  去除题目中的<p></p>获取其他标签，只有部分题目有，可能是尔雅自己整理时候加入的。
            for t in title:
                p_rule = '<.*?>'
                t = re.sub(p_rule, '', t)
                p_rule = '&.*?;'
                t = re.sub(p_rule, '', t)

                print(j, t)
                j += 1


mooc = Mooc()
courseId = '200080607'#input('请输入courseId:')  # '200837021'  200080607 = 189题
if courseId:
    mooc.getTextByCourseId(courseId)
else:
    print('请输入正确的courseId.')
