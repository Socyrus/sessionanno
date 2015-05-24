__author__ = 'defaultstr'
#coding=utf8

from bs4 import BeautifulSoup


def add_character_bounding_box(results):
    res =[]
    _id = 0
    count = 0
    for result in results:
        count = count + 1
        _id, html = process_result(count, _id, result.content)
        res.append('<h2>  结果%d </h2>' % count)
        res.append(html)
    return res


def process_result(count, _id, result):
    soup = BeautifulSoup(result)
    div = soup.find('div')
    #change title
    title = div.find('h3').find('a')
    _id, tag = process_tag(_id, str(title), 'a')
    title.replace_with(tag)
    #change snippet
    snippet = div.select('.ft')[0]
    _id, tag = process_tag(_id, str(snippet), 'div')
    snippet.replace_with(tag)
    #change foot
    foot = div.select('.fb')[0].find('cite')
    _id, tag = process_tag(_id, str(foot), 'cite')
    foot.replace_with(tag)
    return _id, str(div)


def process_tag(_id, html, tag_name):
    soup = BeautifulSoup(html)
    old_tag = soup.find(tag_name)
    old_str = unicode(old_tag)
    new_str = u''
    tmp_str = u''
    level = 0
    print('old_str : %s\n' % old_str)
    for c in old_str:
        if c == u'<':
            level += 1
            new_str += c
        elif c == u'>':
            level -= 1
            new_str += c
        elif level > 0:
            new_str += c
        else:
            if tmp_str == u'':
                if c == u'&':
                    tmp_str = c
                else:
                    new_str += '<span class="character_bound" id=ch_%d>%s</span>' % (_id, c)
                    _id += 1
            else:
                if c == u';':
                    tmp_str += c
                    new_str += '<span class="character_bound" id=ch_%d>%s</span>' % (_id, tmp_str)
                    _id += 1
                    tmp_str = u''
                else:
                    tmp_str += c
    #print new_str
    new_tag = BeautifulSoup(new_str).find(tag_name)
    return _id, new_tag

if __name__ == '__main__':
    html = r"""
    <div class="rb" id="rb_0"> <h3 class="pt"> <!--awbg4--> <a href="http://www.ubao.com/shuyu/jk-28.html" id="uigs__4" name="dttl" target="_blank"><!--awbg4--><em><!--red_beg-->长期护理保险<!--red_end--></em>—保险术语—优保网</a> </h3> <div class="ft" id="cacheresult_summary_4"> <!--summary_beg--><em><!--red_beg-->长期护理保险<!--red_end--></em>是健康保险非常重要的组成部分，在国外比较流行。<em><!--red_beg-->长期护理保险<!--red_end--></em>是因为年老、疾病或伤残而需要长期照顾的被保险人提供护理服务费用的健康保险。一般的医疗或其...<!--summary_end--></div> <div class="fb"> <cite id="cacheresult_info_4">www.ubao.com/shuyu/...&nbsp;-&nbsp;2014-11-30</cite> <!--resultinfodate:2014-11-30-->&nbsp;-&nbsp;<!--resultsnap_beg--><a href="/websnapshot?ie=utf8&amp;url=http%3A%2F%2Fwww.ubao.com%2Fshuyu%2Fjk-28.html&amp;did=920bd74ce708c4ba-81888f63f547478e-92606e8d04d9a32970cd3f5a28940229&amp;k=90dfb3499cbd93176c955e7e5257953c&amp;encodedQuery=%E9%95%BF%E6%9C%9F%E6%8A%A4%E7%90%86%E4%BF%9D%E9%99%A9&amp;query=%E9%95%BF%E6%9C%9F%E6%8A%A4%E7%90%86%E4%BF%9D%E9%99%A9&amp;&amp;num=50&amp;w=01020400&amp;m=0&amp;st=1" id="sogou_snapshot_4" style="color: #666666;" target="_blank">快照<!--resultsnap_end--></a>  &nbsp;-&nbsp;<a href="javascript:void(null);" id="sogou_preview_4" name="sogou_preview_links" onclick="sogou_preview(this,'4');return false;" sogou_preview_link="http://www.ubao.com/shuyu/jk-28.html" sogou_preview_title="<em><!--red_beg-->长期护理保险<!--red_end--></em>—保险术语—优保网" style="color: #666666;" url="/websnapshot?ie=utf8&amp;preview=1&amp;url=http%3A%2F%2Fwww.ubao.com%2Fshuyu%2Fjk-28.html&amp;did=920bd74ce708c4ba-81888f63f547478e-92606e8d04d9a32970cd3f5a28940229&amp;k=90dfb3499cbd93176c955e7e5257953c&amp;encodedQuery=%E9%95%BF%E6%9C%9F%E6%8A%A4%E7%90%86%E4%BF%9D%E9%99%A9&amp;query=%E9%95%BF%E6%9C%9F%E6%8A%A4%E7%90%86%E4%BF%9D%E9%99%A9&amp;&amp;num=50&amp;title=%E9%95%BF%E6%9C%9F%E6%8A%A4%E7%90%86%E4%BF%9D%E9%99%A9%E2%80%94%E4%BF%9D%E9%99%A9%E6%9C%AF%E8%AF%AD%E2%80%94%E4%BC%98%E4%BF%9D%E7%BD%91&amp;st=1">预览</a> <div class="fb-remark"><a class="vr-sp-evaicon" href="javascript:void(0);"><i></i></a><a class="vr-sp-collect" href="javascript:void(0);"><i></i></a><span from="java" id="920bd74ce708c4ba-81888f63f547478e-92606e8d04d9a32970cd3f5a28940229" style="display:none;" zandocid="920bd74ce708c4ba-81888f63f547478e-92606e8d04d9a32970cd3f5a28940229" zantitle="%EE%90%8A%E9%95%BF%E6%9C%9F%E6%8A%A4%E7%90%86%E4%BF%9D%E9%99%A9%EE%90%8B%E2%80%94%E4%BF%9D%E9%99%A9%E6%9C%AF%E8%AF%AD%E2%80%94%E4%BC%98%E4%BF%9D%E7%BD%91" zanurl="http%3A%2F%2Fwww.ubao.com%2Fshuyu%2Fjk-28.html"></span></div><script>initEndorseShow2({"docid":"920bd74ce708c4ba-81888f63f547478e-92606e8d04d9a32970cd3f5a28940229","count":"0"},{"total":"0","docid":"920bd74ce708c4ba-81888f63f547478e-92606e8d04d9a32970cd3f5a28940229","score":"0"});</script></div> <div class="r-sech ext_query" id="sogou_vr__sq_ext_4" style="display:none"><span>推荐您搜索：</span><a href="http://www.sogou.com/web?query=保险术语" id="sogou_vr__sq_ext_a_4" target="_blank">保险术语</a></div> <div class="r-sech site_query" ext="保险术语" id="sogou_vr__sq_ext_site_4" site="" style="display:none"><span>推荐您在<a href="http://www.ubao.com/shuyu/jk-28.html" id="sogou_vr__sq_ext_site_url_4" target="_blank">http://www.ubao.com/shuyu/jk-28.html</a>站内搜索： </span><a href="http://www.ubao.com/shuyu/jk-28.html" id="sogou_vr__sq_ext_stie_a_4" target="_blank"></a></div></div>
    """
    _id, tag = process_result(0, html)
    print _id
    print tag
